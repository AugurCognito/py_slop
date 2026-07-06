"""Detect redundant boolean if/return patterns.

Catches:
  if condition:
      return True
  else:
      return False

  if condition:
      return True
  return False

Use `return condition` (or `return not condition`) directly.
Ruff's SIM103 covers `if x: return True; return False` but not all forms.
This catches the explicit else variant too.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "redundant-boolean-return"


def _is_return_bool(node: ast.stmt) -> bool:
    if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
        return isinstance(node.value.value, bool)
    return False


def check_redundant_boolean_return(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue

        if not node.orelse:
            continue

        consequent = node.body
        alternate = node.orelse

        if len(consequent) == 1 and len(alternate) == 1:
            if _is_return_bool(consequent[0]) and _is_return_bool(alternate[0]):
                violations.append(
                    Violation(
                        line=node.lineno,
                        col=node.col_offset,
                        comment=f"redundant boolean if/return at line {node.lineno}",
                    )
                )

    return violations
