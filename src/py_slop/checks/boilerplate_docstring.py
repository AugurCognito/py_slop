"""Detect boilerplate docstrings that restate the function signature.

Catches:
  def get_user(user_id: int) -> User:
      \"\"\"Get the user.\"\"\"

  def create_order(data: dict) -> Order:
      \"\"\"Create an order.

      Args:
          data: The data.
      \"\"\"

Ruff's D-series checks formatting, not whether the content is useful.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass

RESTATE_PATTERN = re.compile(
    r'^(?:(?:get|set|create|delete|update|fetch|find|check|validate|process|handle|parse|'
    r'build|make|generate|compute|calculate|convert|transform|init|initialize|setup|'
    r'load|save|send|receive|add|remove|insert|append|pop|push|start|stop|open|close|run|execute)'
    r'\s+(?:the\s+)?)?(\w+)',
    re.IGNORECASE,
)

BOILERPLATE_ARG_DESCRIPTIONS = re.compile(
    r"^\s*\w+\s*(?:\([^)]*\))?\s*:\s*(?:the|a|an)?\s*\w+\.?\s*$",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class Violation:
    line: int
    col: int
    comment: str
    check: str = "boilerplate-docstring"


def _func_name_words(name: str) -> set[str]:
    parts = re.split(r"_+", name.lower())
    return {p for p in parts if len(p) > 2}


def check_boilerplate_docstrings(source: str, filename: str = "<stdin>") -> list[Violation]:
    violations: list[Violation] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        docstring = ast.get_docstring(node, clean=True)
        if not docstring:
            continue

        first_line = docstring.strip().split("\n")[0].rstrip(".")
        name_words = _func_name_words(node.name)

        if not name_words:
            continue

        doc_words = {w.lower() for w in re.findall(r"\w+", first_line) if len(w) > 2}
        overlap = name_words & doc_words

        if len(overlap) >= len(name_words) * 0.7 and len(first_line.split()) <= 6:
            line = node.lineno
            violations.append(
                Violation(line=line, col=node.col_offset, comment=f'"""{first_line}..."""')
            )

    return violations
