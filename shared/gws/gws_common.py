#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RATE_LIMIT = 30  # calls per minute
CACHE_DIR = Path.home() / ".cache" / "gws-wrapper"
RATE_FILE = CACHE_DIR / "rate.json"
LOG_DIR = Path(__file__).parent.parent / "logs"


class RateLimiter:
    def __init__(self, calls_per_min=RATE_LIMIT):
        self.calls_per_min = calls_per_min
        self.window_secs = 60

    def check(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        now = datetime.now().timestamp()
        state = {"calls": 0, "window_start": now}

        if RATE_FILE.exists():
            try:
                state = json.loads(RATE_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                pass

        elapsed = now - state["window_start"]
        if elapsed >= self.window_secs:
            state["calls"] = 0
            state["window_start"] = now

        if state["calls"] >= self.calls_per_min:
            reset_in = self.window_secs - elapsed
            sys.exit(f"Rate limit exceeded: {self.calls_per_min} calls/min. Reset in {reset_in:.0f}s.")

        state["calls"] += 1
        RATE_FILE.write_text(json.dumps(state))


def confirm(prompt):
    if not sys.stdin.isatty():
        sys.exit("Confirmation required but stdin is not a TTY.")
    try:
        response = input(f"{prompt} [y/N] ").strip().lower()
        return response == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def log(service, args, status, note=""):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "gws.log"

    entry = {
        "ts": datetime.now().isoformat(),
        "service": service,
        "args": args,
        "status": status,
        "note": note,
    }
    with log_file.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def run_gws(service, args, dry_run=False):
    cmd = ["gws", service]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(args)

    return subprocess.run(cmd)
