# Maze Solver with Python

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package_manager-DE5FE9?logo=uv&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![Pylint](https://img.shields.io/badge/pylint-enabled-yellowgreen?logo=python&logoColor=white)
![Mypy](https://img.shields.io/badge/mypy-checked-blue?logo=python&logoColor=white)
![Bandit](https://img.shields.io/badge/bandit-security-orange?logo=python&logoColor=white)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Sphinx](https://img.shields.io/badge/docs-sphinx-blue?logo=sphinx&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

> A **maze generator and solver** built with Python and **tkinter**.  
> Mazes are generated with randomised recursive backtracking and solved with depth-first search, animated in real time.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Development](#development)
- [Documentation](#documentation)

---

## Prerequisites

- Python 3.12 (via [pyenv](https://github.com/pyenv/pyenv))
- [uv](https://docs.astral.sh/uv/)

---

## Setup

```bash
pyenv local 3.12.9
uv sync --all-groups
uv run pre-commit install
```

---

## Usage

```bash
uv run maze
```

An 800 × 600 window opens. The maze is drawn cell by cell as it is generated, then a red path traces the solution. Backtracked steps are shown in grey.

---

## How it works

| Phase | Algorithm | Entry point |
|-------|-----------|-------------|
| Generation | Randomised recursive backtracking (DFS) | `Maze._break_walls_r` |
| Solving | Depth-first search | `Maze.solve` |

The grid is stored column-major as `_cells[col][row]`. The entrance is the top wall of `_cells[0][0]`; the exit is the bottom wall of `_cells[-1][-1]`. Pass a `seed` to `Maze` for reproducible layouts.

---

## Development

### Run tests

```bash
uv run pytest -vvs --cov=maze_solver_with_python maze_solver_with_python/tests/
```

Run a single test:

```bash
uv run pytest -vvs maze_solver_with_python/tests/test_maze.py::test_maze_solve_returns_true
```

### Lint & type-check

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pylint maze_solver_with_python/
uv run mypy .
uv run bandit -r . -c pyproject.toml
```

### All checks at once

```bash
pre-commit run --all-files
```

---

## Documentation

Build the HTML docs locally:

```bash
uv run sphinx-build -b html docs/ docs/_build/html
```

Or use autobuild with live reload:

```bash
uv run sphinx-autobuild docs/ docs/_build/html
```
