# Maze Solver with Python

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package_manager-DE5FE9?logo=uv&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![License](https://img.shields.io/badge/license-MIT-green)

> A **maze generator and solver** built with Python and **tkinter**. The maze is generated using a randomised recursive backtracking algorithm and solved with a depth-first search, animated in a GUI window.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)

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

A window (800×600) opens showing the maze being generated and then solved step by step.

---

## Development

### Tests

```bash
uv run pytest -vvs --cov=maze_solver_with_python maze_solver_with_python/tests/
```

### Linting & type checking

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
