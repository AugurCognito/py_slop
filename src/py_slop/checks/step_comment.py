"""Detect step-numbered comments indicating a function does too much.

Catches:
  # Step 1: validate input
  # Step 2: process data

Numbered steps mean the function should be split.
Ruff has no rule for this — it's comment content analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

STEP_PATTERN = re.compile(r"^#\s*step\s+\d+", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "step-comment"


def check_step_comments(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    for i, raw_line in enumerate(source.splitlines(), 1):
        stripped = raw_line.lstrip()
        if not stripped.startswith("#"):
            continue
        if STEP_PATTERN.match(stripped):
            col = len(raw_line) - len(stripped)
            violations.append(Violation(line=i, col=col, comment=stripped))

    return violations
