#!/usr/bin/env python3
"""
Sermon Outline Skill helper — reads a source transcript and prints its
contents so Claude can generate a sermon-only outline. Also resolves the
correct output path.

Usage:
    python sermon-outline.py <source-file> [--path-only]

Output path convention:
    {id}-{slug}-claude-transcript.txt  →  {id}-{slug}-claude-sermon-outline.md
    anything-else.txt                  →  anything-else-claude-sermon-outline.md
"""

import re
import sys
from pathlib import Path


def resolve_output_path(source: Path) -> Path:
    stem = source.stem
    stem = re.sub(r"-claude-\w+$", "", stem)
    return source.parent / f"{stem}-claude-sermon-outline.md"


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    path_only = "--path-only" in sys.argv
    source_arg = next(a for a in sys.argv[1:] if not a.startswith("--"))
    source = Path(source_arg).expanduser().resolve()

    if not source.exists():
        print(f"Error: file not found: {source}", file=sys.stderr)
        sys.exit(1)

    output = resolve_output_path(source)

    if path_only:
        print(output)
        return

    print(f"Source: {source}")
    print(f"Output: {output}")
    print("-" * 60)
    print(source.read_text())


if __name__ == "__main__":
    main()
