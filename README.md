# Maze Solver with Python

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/poetry-package_manager-60A5FA?logo=poetry&logoColor=white)
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
- [Poetry](https://python-poetry.org/)

---

## Setup

```bash
pyenv local 3.12.9
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
pip install -e .
```

---

## Usage

```bash
maze
```

A window (800×600) opens showing the maze being generated and then solved step by step.

---

## Development

### Tests

```bash
./scripts/test.sh
```

### Linting & type checking

```bash
ruff check .
pylint maze_solver_with_python/
mypy .
bandit -r maze_solver_with_python/ -c pyproject.toml
```

### All checks at once

```bash
pre-commit run --all-files
```
