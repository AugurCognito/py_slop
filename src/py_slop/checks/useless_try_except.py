"""Detect try/except that only re-raises the caught exception.

Catches:
  try:
      do_something()
  except Exception as e:
      raise e

The try/except is redundant — let the error propagate naturally.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "useless-try-except"


def check_useless_try_except(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        if node.finalbody:
            continue
        if len(node.handlers) != 1:
            continue

        handler = node.handlers[0]
        if handler.name is None:
            continue
        if len(handler.body) != 1:
            continue

        stmt = handler.body[0]
        if not isinstance(stmt, ast.Raise):
            continue
        if stmt.exc is None:
            continue
        if isinstance(stmt.exc, ast.Name) and stmt.exc.id == handler.name:
            violations.append(
                Violation(
                    line=node.lineno,
                    col=node.col_offset,
                    comment=f"useless try/except at line {node.lineno}",
                )
            )

    return violations
