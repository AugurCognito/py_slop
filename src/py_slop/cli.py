"""CLI entry point for py-slop."""

from __future__ import annotations

import sys
from pathlib import Path

from py_slop.checks import ALL_CHECKS


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] != "check":
        print("Usage: py-slop check <file> [<file> ...]", file=sys.stderr)
        sys.exit(2)

    files = sys.argv[2:]
    if not files:
        print("Error: no files specified", file=sys.stderr)
        sys.exit(2)

    found = 0
    for filepath in files:
        path = Path(filepath)
        if not path.is_file():
            print(f"Error: {filepath} is not a file", file=sys.stderr)
            sys.exit(2)

        source = path.read_text(encoding="utf-8")
        for check_fn in ALL_CHECKS:
            violations = check_fn(source, filename=filepath)
            for v in violations:
                print(f"{filepath}:{v.line}:{v.col}: [{v.check}] {v.comment}")
                found += 1

    if found:
        print(f"\n{found} violation(s) found.", file=sys.stderr)
        sys.exit(1)
