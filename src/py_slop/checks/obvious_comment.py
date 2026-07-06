"""Detect obvious comments that restate what the code does.

Catches patterns like:
  # Increment counter
  counter += 1

  # Return the result
  return result

Short verb-phrase comments that add no information.
Ruff's ERA001 catches commented-out code, not semantic redundancy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

VERB_ARTICLE_PATTERN = re.compile(
    r"^#\s*[A-Z][a-z]+\s+(?:the|a|an|this|all|each|every)\s+\w+",
)

KEEPER_PATTERNS = [
    re.compile(r"\b(?:TODO|FIXME|HACK|NOTE|WARN|XXX|BUG)\b", re.IGNORECASE),
    re.compile(r"\b(?:because|since|workaround|constraint|invariant|N\+1|timeout|retry)\b", re.IGNORECASE),
    re.compile(r"\d{2,}"),
    re.compile(r"(?:noqa|type:\s*ignore|pylint|pragma)", re.IGNORECASE),
]

MAX_COMMENT_LENGTH = 60


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "obvious-comment"


def check_obvious_comments(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    for i, raw_line in enumerate(source.splitlines(), 1):
        stripped = raw_line.lstrip()
        if not stripped.startswith("#"):
            continue
        if len(stripped) > MAX_COMMENT_LENGTH:
            continue
        if not VERB_ARTICLE_PATTERN.match(stripped):
            continue
        if any(p.search(stripped) for p in KEEPER_PATTERNS):
            continue

        col = len(raw_line) - len(stripped)
        violations.append(Violation(line=i, col=col, comment=stripped))

    return violations
