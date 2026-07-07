# py-slop

[![PyPI](https://img.shields.io/pypi/v/py-slop.svg)](https://pypi.org/project/py-slop/)

Linter that catches AI-generated code slop in Python.

Deep, single-ecosystem checks for patterns that LLMs produce but experienced
Python developers don't — narrator comments, silent exception swallowing,
boilerplate docstrings, N+1 query loops, and more.

Modeled on [ex_slop](https://github.com/elixir-vibe/ex_slop) (40 Credo checks
for Elixir). Where ex_slop integrates with Credo, py-slop ships as a standalone
CLI and pre-commit hook. Ruff already covers the classics (E722, S110, B006,
PGH003) — py-slop targets what ruff *cannot* express.

## Installation

```bash
pip install py-slop
```

## Usage

```bash
py-slop check path/to/file.py [more files...]
```

### pre-commit

```yaml
repos:
  - repo: https://github.com/AugurCognito/py_slop
    rev: v0.1.1
    hooks:
      - id: py-slop
```

## Checks

### Comment / docstring content (ruff can't — it never inspects content)

| Check | What it catches | Nearest ruff rule |
|-------|----------------|-------------------|
| `narrator-comment` | `# First, we validate the input` / `# Here we fetch` | None — ERA001 catches commented-out code, not narration |
| `obvious-comment` | `# Fetch the user` above `user = get_user(id)` | None |
| `step-comment` | `# Step 1: validate` / `# Step 2: process` | None |
| `boilerplate-docstring` | `def get_user(id): """Get the user."""` | D-series checks formatting, not semantic redundancy |

### Error handling (beyond ruff's scope)

| Check | What it catches | Nearest ruff rule |
|-------|----------------|-------------------|
| `except-returns-default` | `except: return None` / `""` / `0` / `False` / `[]` / `{}` | BLE001 flags blanket `except:`, not what it *returns* |
| `except-log-continue` | `except Exception as e: logger.error(e)` — logs but swallows | None — behavioral analysis of except bodies |
| `useless-try-except` | `try: f() except e: raise e` — redundant wrapper | TRY302 is similar but not identical |

### Patterns

| Check | What it catches | Nearest ruff rule |
|-------|----------------|-------------------|
| `query-in-loop` | N+1 queries in loops (Django `objects.*`, SQLAlchemy `session.*`) | None — no framework-aware detection |
| `redundant-boolean-return` | `if x: return True; else: return False` | SIM103 covers the no-else form; this catches explicit else |

## Ruff overlap honesty

Run ruff for these — py-slop deliberately does not duplicate them:

| Pattern | Ruff rule |
|---------|-----------|
| Blanket `except:` | BLE001 |
| Bare `except Exception:` + `pass` | S110 |
| `print()` left behind | T201 |
| Commented-out code | ERA001 |
| Blanket `type: ignore` | PGH003 |
| Mutable default arguments | B006 |

## License

[MIT](LICENSE)
