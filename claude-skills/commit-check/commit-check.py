#!/usr/bin/env python3
"""
commit-check: scan git staged changes for secrets, PII, hardcoded credentials,
AWS account numbers, and local filesystem paths before committing.

Exit code 0 = clean. Exit code 1 = findings (use as pre-commit hook).

Usage:
    python commit-check.py              # check staged changes
    python commit-check.py --diff       # read diff from stdin
    python commit-check.py --all        # check all tracked files (not just staged)
"""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

@dataclass
class Pattern:
    name: str
    regex: str
    severity: str          # "error" | "warning"
    description: str
    allowlist: list[str] = None  # substrings that suppress the match


PATTERNS: list[Pattern] = [

    # --- Credentials & secrets ---
    Pattern("aws_access_key",      r'\bAKIA[0-9A-Z]{16}\b',                        "error",   "AWS access key ID"),
    Pattern("aws_secret_key",      r'(?i)aws.{0,20}secret.{0,20}[=:]\s*["\']?[A-Za-z0-9/+]{40}', "error", "AWS secret access key"),
    Pattern("github_token",        r'\bghp_[A-Za-z0-9]{36}\b',                     "error",   "GitHub personal access token"),
    Pattern("github_token_v2",     r'\bgithub_pat_[A-Za-z0-9_]{82}\b',             "error",   "GitHub fine-grained token"),
    Pattern("generic_api_key",     r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{16,}', "error", "Generic API key assignment",
            allowlist=["your_api_key", "YOUR_API_KEY", "example", "placeholder", "REPLACE", "os.getenv", "os.environ", "ENV["]),
    Pattern("generic_secret",      r'(?i)(secret|password|passwd|pwd)\s*[=:]\s*["\'][^"\']{6,}["\']', "error", "Hardcoded secret/password",
            allowlist=["your_", "example", "placeholder", "REPLACE", "test", "dummy", "fake", "changeme"]),
    Pattern("bearer_token",        r'(?i)bearer\s+[A-Za-z0-9\-._~+/]{20,}',       "error",   "Bearer token"),
    Pattern("private_key_header",  r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY', "error",   "Private key"),
    Pattern("slack_token",         r'\bxox[baprs]-[0-9A-Za-z\-]{10,}',             "error",   "Slack token"),
    Pattern("stripe_key",          r'\b(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}\b',"error",   "Stripe API key"),
    Pattern("sendgrid_key",        r'\bSG\.[A-Za-z0-9\-_]{22}\.[A-Za-z0-9\-_]{43}\b', "error", "SendGrid API key"),
    Pattern("jwt",                 r'\beyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\b', "warning", "JWT token"),

    # --- AWS account numbers ---
    Pattern("aws_account_id",      r'\b\d{12}\b',                                  "warning", "Possible AWS account ID (12-digit number)",
            allowlist=["#", "//", "example", "123456789012", "000000000000"]),

    # --- PII ---
    Pattern("email",               r'\b[a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', "warning", "Email address",
            allowlist=["example.com", "test.com", "noreply@", "user@example", "foo@bar", "@anthropic.com", "noqa"]),
    Pattern("phone_us",            r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b', "warning", "US phone number"),
    Pattern("ssn",                 r'\b\d{3}-\d{2}-\d{4}\b',                       "error",   "Social Security Number"),
    Pattern("credit_card",         r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b', "error", "Credit card number"),

    # --- Local filesystem paths ---
    Pattern("home_dir_users",      r'/Users/[A-Za-z][A-Za-z0-9_.-]+/',             "error",   "macOS /Users/<name>/ path",
            allowlist=["/Users/runner/", "/Users/user/", "/Users/ubuntu/", "/Users/actions/"]),
    Pattern("home_dir_home",       r'/home/[A-Za-z][A-Za-z0-9_.-]+/',              "error",   "Linux /home/<name>/ path",
            allowlist=["/home/runner/", "/home/user/", "/home/ubuntu/", "/home/actions/"]),
    Pattern("tilde_path",          r'~(?:/[A-Za-z]|\s*/[A-Za-z])',                 "warning", "Tilde-expanded home path (~/...)",
            allowlist=["~/.ssh/known_hosts", "~/.bashrc", "~/.zshrc", "~/.profile",
                       "example", "your_home", "YOUR_HOME"]),
    Pattern("windows_user_path",   r'C:\\Users\\[A-Za-z][A-Za-z0-9_.-]+\\',       "error",   "Windows C:\\Users\\<name>\\ path"),

    # --- Specific personal path fragments ---
    Pattern("personal_code_dir",   r'(?i)/code/[a-z]',                             "warning", "Hardcoded ~/code/ project path — use relative paths",
            allowlist=["# example", "YOUR_PATH", "your_path"]),
]

# File extensions to skip
SKIP_EXTENSIONS = {
    ".pyc", ".pyo", ".so", ".o", ".a", ".lib", ".dll", ".exe", ".bin",
    ".jar", ".class", ".wasm", ".png", ".jpg", ".jpeg", ".gif", ".ico",
    ".svg", ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".zip",
    ".tar", ".gz", ".lock",
}

# Paths to skip entirely
SKIP_PATHS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules",
    ".venv", "venv", "env", "dist", "build", ".mypy_cache",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    file: str
    line: int
    pattern: Pattern
    matched: str
    context: str


def should_skip(filepath: str) -> bool:
    p = Path(filepath)
    if p.suffix.lower() in SKIP_EXTENSIONS:
        return True
    return any(part in SKIP_PATHS for part in p.parts)


def is_allowlisted(pattern: Pattern, line: str, matched: str) -> bool:
    if not pattern.allowlist:
        return False
    return any(a.lower() in line.lower() for a in pattern.allowlist)


def scan_diff(diff: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = diff.split("\n")
    current_file: Optional[str] = None
    line_num = 0

    for line in lines:
        if line.startswith("+++ b/"):
            current_file = line[6:]
            line_num = 0
            continue
        if line.startswith("+++ /dev/null"):
            current_file = None
            continue
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            line_num = int(m.group(1)) - 1 if m else 0
            continue

        if line.startswith("+") and not line.startswith("+++"):
            line_num += 1
            if not current_file or should_skip(current_file):
                continue
            content = line[1:]
            # Skip comment-only lines that are clearly docs/examples
            stripped = content.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                # Still check for hardcoded secrets in comments, but skip path allowlist hits
                pass
            for pat in PATTERNS:
                for m in re.finditer(pat.regex, content):
                    matched = m.group()
                    if is_allowlisted(pat, content, matched):
                        continue
                    start = max(0, m.start() - 25)
                    end = min(len(content), m.end() + 25)
                    context = content[start:end].strip()
                    findings.append(Finding(current_file, line_num, pat, matched, context))
        elif line.startswith(" "):
            line_num += 1

    return findings


def get_staged_diff() -> str:
    r = subprocess.run(["git", "diff", "--cached", "--unified=0"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("Error: not in a git repo or no staged changes", file=sys.stderr)
        sys.exit(1)
    return r.stdout


def get_full_diff() -> str:
    r = subprocess.run(["git", "diff", "HEAD", "--unified=0"],
                       capture_output=True, text=True)
    return r.stdout


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

SEVERITY_ICON = {"error": "🔴", "warning": "🟡"}


def print_findings(findings: list[Finding], source: str) -> int:
    errors   = [f for f in findings if f.pattern.severity == "error"]
    warnings = [f for f in findings if f.pattern.severity == "warning"]

    if not findings:
        print(f"✅  No issues found in {source}")
        return 0

    print(f"\n{'='*60}")
    print(f"  commit-check: {len(errors)} error(s), {len(warnings)} warning(s)")
    print(f"{'='*60}\n")

    # Group by file
    by_file: dict[str, list[Finding]] = {}
    for f in sorted(findings, key=lambda x: (x.pattern.severity, x.file, x.line)):
        by_file.setdefault(f.file, []).append(f)

    for filepath, file_findings in by_file.items():
        print(f"  📄 {filepath}")
        for f in file_findings:
            icon = SEVERITY_ICON[f.pattern.severity]
            print(f"     {icon} Line {f.line:>4}  [{f.pattern.name}]  {f.pattern.description}")
            print(f"            match:   {f.matched!r}")
            print(f"            context: ...{f.context}...")
        print()

    if errors:
        print("❌  Errors must be resolved before committing.")
        print("    To unstage a file:  git restore --staged <file>")
    else:
        print("⚠️   Warnings found — review before committing.")

    print()
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Scan git changes for secrets and PII")
    parser.add_argument("--stdin", action="store_true", help="Read diff from stdin")
    parser.add_argument("--all",   action="store_true", help="Check all tracked files via HEAD diff")
    args = parser.parse_args()

    if args.stdin:
        diff = sys.stdin.read()
        source = "stdin"
    elif args.all:
        diff = get_full_diff()
        source = "all tracked files"
    else:
        diff = get_staged_diff()
        source = "staged changes"

    if not diff.strip():
        print(f"  No changes in {source}")
        sys.exit(0)

    findings = scan_diff(diff)
    exit_code = print_findings(findings, source)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
