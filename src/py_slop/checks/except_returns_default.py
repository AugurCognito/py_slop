"""Detect except blocks that return a silent default value.

Catches:
  except Exception:
      return None

  except ValueError:
      return ""

  except KeyError:
      return []

Ruff's BLE001 only flags blanket `except:` — this flags the *behavior* of
returning silent defaults regardless of specificity.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "except-returns-default"


_SILENT_DEFAULTS = {type(None), str, int, float, bool}


def _is_silent_default(node: ast.expr) -> bool:
    if isinstance(node, ast.Constant):
        if node.value is None:
            return True
        if isinstance(node.value, (str, int, float, bool)) and not node.value:
            return True
    if isinstance(node, ast.List) and len(node.elts) == 0:
        return True
    if isinstance(node, ast.Dict) and len(node.keys) == 0:
        return True
    if isinstance(node, ast.Tuple) and len(node.elts) == 0:
        return True
    return False


def check_except_returns_default(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.Return) and stmt.value is not None and _is_silent_default(stmt.value):
                violations.append(
                    Violation(
                        line=stmt.lineno,
                        col=stmt.col_offset,
                        comment=f"except returns silent default at line {stmt.lineno}",
                    )
                )

    return violations
