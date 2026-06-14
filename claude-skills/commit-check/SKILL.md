# commit-check

Scan git staged changes for secrets, PII, hardcoded credentials, AWS account numbers, and local filesystem paths before committing.

## Invocation

```
/commit-check
```

## What it detects

**Errors** (block commit):
- AWS access keys (`AKIA...`) and secret keys
- GitHub tokens (`ghp_`, `github_pat_`)
- Generic hardcoded API keys and passwords
- Bearer tokens, private keys, Slack/Stripe/SendGrid tokens
- Social Security Numbers, credit card numbers
- macOS `/Users/<name>/` and Linux `/home/<name>/` paths
- Windows `C:\Users\<name>\` paths

**Warnings** (review before committing):
- Possible AWS account IDs (12-digit numbers)
- Email addresses
- US phone numbers
- Tilde-expanded home paths (`~/...`)
- Hardcoded project paths (`/code/...`)
- JWTs

## Usage

```bash
# Check staged changes (default)
python commit-check.py

# Check all tracked files
python commit-check.py --all

# Pipe a diff
git diff HEAD~1 | python commit-check.py --stdin
```

## As a pre-commit hook

```bash
ln -s /path/to/commit-check.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Exit code 0 = clean. Exit code 1 = errors found (warnings alone return 0).
