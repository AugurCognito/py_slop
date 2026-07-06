"""Detect narrator-style comments that LLMs produce but humans don't write.

Catches patterns like:
  # First, we validate the input
  # Here we fetch the user
  # Now we process the data
  # Let's create the response

These narrate what code does step-by-step — a hallmark of AI-generated slop.
Ruff cannot express this check because it never inspects comment *content*.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

import libcst as cst

NARRATOR_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"#\s*(?:first|next|then|now|here|finally|lastly|after that)[,:]?\s+"
        r"(?:we|let'?s|i)\s+",
        re.IGNORECASE,
    ),
    re.compile(r"#\s*(?:we|let'?s)\s+(?:need to|want to|have to|should|will|can|must)\s+", re.IGNORECASE),
    re.compile(r"#\s*(?:we|let'?s)\s+\w+\s+the\s+", re.IGNORECASE),
    re.compile(r"#\s*(?:step\s+\d+)", re.IGNORECASE),
]


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "narrator-comment"


def _extract_comments(source: str) -> list[tuple[int, int, str]]:
    """Extract (line, col, text) for every comment in source using libcst's tokenizer."""
    try:
        tokens = cst.parse_module(source)
    except cst.ParserSyntaxError:
        return []

    results: list[tuple[int, int, str]] = []

    class CommentCollector(cst.CSTVisitor):
        def _visit_comment(self, comment: cst.Comment, line: int) -> None:
            results.append((line, 0, comment.value))

        def visit_EmptyLine(self, node: cst.EmptyLine) -> None:
            if node.comment is not None:
                pos = node.comment
                results.append((0, 0, pos.value))

        def visit_TrailingWhitespace(self, node: cst.TrailingWhitespace) -> None:
            if node.comment is not None:
                results.append((0, 0, node.comment.value))

    tokens.walk(CommentCollector())

    if not results:
        for i, line in enumerate(source.splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                col = len(line) - len(stripped)
                results.append((i, col, stripped))

    return results


def check_narrator_comments(source: str, filename: str = "<stdin>") -> list[Violation]:
    """Return narrator-comment violations found in source."""
    violations: list[Violation] = []

    for line_num, (i, raw_line) in enumerate(
        enumerate(source.splitlines(), 1), 0
    ):
        stripped = raw_line.lstrip()
        if not stripped.startswith("#"):
            continue
        for pattern in NARRATOR_PATTERNS:
            if pattern.search(stripped):
                col = len(raw_line) - len(stripped)
                violations.append(Violation(line=i, col=col, comment=stripped))
                break

    return violations


class NarratorCommentChecker:
    """Public API for the narrator-comment check."""

    name = "narrator-comment"
    description = "Narrator-style comments that narrate code step-by-step"

    @staticmethod
    def run(source: str, filename: str = "<stdin>") -> list[Violation]:
        return check_narrator_comments(source, filename)
