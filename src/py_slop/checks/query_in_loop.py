"""Detect database queries inside loops (N+1 pattern).

Catches:
  for user in users:
      orders = Order.objects.filter(user=user)  # Django

  for user in users:
      session.query(Order).filter_by(user_id=user.id)  # SQLAlchemy

Ruff has no framework-aware N+1 detection.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass

DJANGO_QUERY_ATTRS = {
    "filter", "exclude", "get", "all", "first", "last",
    "create", "get_or_create", "update_or_create", "values", "values_list",
    "annotate", "aggregate", "count", "exists", "delete", "update",
    "select_related", "prefetch_related",
}

SQLALCHEMY_QUERY_PATTERNS = {"query", "execute", "scalar", "scalars"}


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "query-in-loop"


def _is_query_call(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Attribute):
        if func.attr in DJANGO_QUERY_ATTRS:
            if isinstance(func.value, ast.Attribute) and func.value.attr == "objects":
                return True
        if func.attr in SQLALCHEMY_QUERY_PATTERNS:
            return True
    return False


def _walk_for_queries(body: list[ast.stmt]) -> list[tuple[int, int]]:
    seen: set[int] = set()
    results: list[tuple[int, int]] = []
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                continue
            if not isinstance(node, (ast.Expr, ast.Assign)):
                continue
            value = node.value if isinstance(node, (ast.Expr, ast.Assign)) else None
            if value is not None and _is_query_call(value) and node.lineno not in seen:
                seen.add(node.lineno)
                results.append((node.lineno, node.col_offset))
    return results


def check_query_in_loop(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            for line, col in _walk_for_queries(node.body):
                violations.append(
                    Violation(
                        line=line,
                        col=col,
                        comment=f"database query inside loop at line {line}",
                    )
                )

    return violations
