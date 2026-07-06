# py-slop

Linter that catches AI-generated code slop in Python.

Deep, single-ecosystem checks for patterns that LLMs produce but experienced
Python developers don't — narrator comments, silent exception swallowing,
docstrings that restate the signature, N+1 query loops, and more.

Modeled on [ex_slop](https://github.com/elixir-vibe/ex_slop) (40 Credo checks
for Elixir). Where ex_slop integrates with Credo, py-slop ships as a standalone
CLI and pre-commit hook. Ruff already covers the classics (E722, S110, B006,
PGH003) — py-slop targets what ruff *cannot* express: checks that inspect
comment/docstring **content**, cross-statement semantics, and framework-aware
anti-patterns.

## Status

**v0.0.x** — name-establishing release, API unstable. One working check ships
today; a full audit against ruff's rule set will determine the v0.1.0 scope.
See the roadmap below.

## Installation

```bash
pip install py-slop
```

## Usage

```bash
py-slop check path/to/file.py [more files...]
```

### pre-commit (coming in v0.1.0)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/augurcognito/py_slop
    rev: v0.1.0
    hooks:
      - id: py-slop
```

## Checks

| Check | What it catches | Why ruff can't |
|-------|----------------|----------------|
| `narrator-comment` | `# First, we validate the input` / `# Here we fetch the user` / `# Step 1:` | Ruff never inspects comment *content* — only structure (ERA001 catches commented-out code, not narration) |

## Roadmap (v0.1.0, contingent on ruff coverage audit)

- `docstring-restates-signature` — `def get_user(id): """Get the user by id."""`
- `except-returns-silent-default` — `except: return None` beyond BLE001 scope
- `query-in-loop` — N+1 queries in loops (Django/SQLAlchemy aware)
- `obvious-comment` — `# Increment counter` above `counter += 1`
- `step-comment` — `# Step 1: ...` / `# Step 2: ...`
- `boilerplate-docstring-params` — `Args: x: The x value`

Each check will ship with an honest "ruff already covers X" overlap table.

## License

[MIT](LICENSE)
