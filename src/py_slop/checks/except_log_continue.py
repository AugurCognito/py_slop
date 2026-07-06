"""Detect except blocks that only log the error and continue.

Catches:
  except Exception as e:
      logger.error(e)

  except ValueError as e:
      print(f"Error: {e}")

Logging is not handling. If nothing can be done, let the error propagate.
Ruff has no check for this — it's behavioral analysis of except bodies.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass

LOGGING_NAMES = {"print", "logging", "logger", "log"}
LOGGING_METHODS = {"debug", "info", "warning", "warn", "error", "critical", "exception", "fatal"}


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "except-log-continue"


def _is_logging_call(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name) and func.id == "print":
        return True
    if isinstance(func, ast.Attribute) and func.attr in LOGGING_METHODS:
        if isinstance(func.value, ast.Name) and func.value.id.lower() in LOGGING_NAMES:
            return True
    return False


def check_except_log_continue(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        body = node.body
        if not body:
            continue

        has_logging = False
        has_raise = False
        has_return = False
        all_logging = True

        for stmt in body:
            if isinstance(stmt, ast.Raise):
                has_raise = True
                all_logging = False
            elif isinstance(stmt, ast.Return):
                has_return = True
                all_logging = False
            elif isinstance(stmt, ast.Expr) and _is_logging_call(stmt.value):
                has_logging = True
            else:
                all_logging = False

        if has_logging and all_logging and not has_raise and not has_return:
            violations.append(
                Violation(
                    line=node.lineno,
                    col=node.col_offset,
                    comment=f"except block only logs at line {node.lineno}",
                )
            )

    return violations
