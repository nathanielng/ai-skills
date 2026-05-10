#!/usr/bin/env python3
import sys
from gws_common import RateLimiter, confirm, log, run_gws

DESTRUCTIVE = {
    "+send",
    "+reply",
    "+reply-all",
    "+forward",
    "messages.delete",
    "messages.trash",
    "messages.modify",
    "drafts.delete",
    "labels.delete",
    "threads.delete",
    "threads.modify",
    "threads.trash",
}


def is_destructive(args):
    args_str = " ".join(args)
    for pattern in DESTRUCTIVE:
        if pattern in args_str:
            return True
    return False


def main():
    args = sys.argv[1:]
    force = "--force" in args
    dry_run_only = "--dry-run-only" in args

    if force:
        args = [a for a in args if a != "--force"]
    if dry_run_only:
        args = [a for a in args if a != "--dry-run-only"]

    try:
        RateLimiter().check()
    except SystemExit as e:
        log("gmail", args, "error", str(e))
        raise

    is_dest = is_destructive(args)

    if is_dest and not dry_run_only and not force:
        print("[DRY RUN]")
        run_gws("gmail", args, dry_run=True)
        print()

        if not confirm("Execute for real?"):
            log("gmail", args, "skipped", "User declined after dry-run")
            return

    result = run_gws("gmail", args, dry_run=dry_run_only)

    status = "ok" if result.returncode == 0 else "error"
    log("gmail", args, status, f"exit code {result.returncode}")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
