# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the GUI app
uv run maze

# Run tests with coverage
uv run pytest -vvs --cov=maze_solver_with_python maze_solver_with_python/tests/

# Run a single test
uv run pytest -vvs maze_solver_with_python/tests/test_maze.py::test_maze_solve_returns_true

# Lint and format
uv run ruff check --fix .
uv run ruff format .
uv run pylint maze_solver_with_python/
uv run mypy .
uv run bandit -r . -c pyproject.toml

# Run all pre-commit checks at once
pre-commit run --all-files

# Build Sphinx HTML docs
uv run sphinx-build -b html docs/ docs/_build/html

# Live-reload docs
uv run sphinx-autobuild docs/ docs/_build/html

# Build standalone executable (output: dist/maze-solver)
bash scripts/build_exe.sh

# Docker — build and run with X11 forwarding
xhost +local:docker
docker compose up --build
```

## Architecture

All logic lives in `maze_solver_with_python/core/models.py`. There are no submodules beyond `core/`.

**Class hierarchy and responsibilities:**

- `Point(x, y)` — coordinate primitive used by everything else
- `Line(p1, p2)` — draws itself onto a `Canvas` via `line.draw(canvas, fill_color)`
- `Window` — wraps `tkinter.Tk` + `Canvas`; exposes `draw_line()`, `redraw()`, `wait_for_close()`; `win=None` means headless (used in tests)
- `Cell(top_left, right_bottom, win, **kwargs)` — a single maze cell. Wall presence is stored in `cell.configs` dict with keys `"left"`, `"right"`, `"top"`, `"bottom"` (bool, `True` = wall present). `cell.visited` tracks DFS state. `draw_move(to_cell, undo=False)` draws a red path line (grey when undoing).
- `Maze` — owns a 2-D list `_cells[col][row]` (x-axis first, then y-axis). Construction pipeline:
  1. `_create_cells()` — fills the grid and draws each cell
  2. `_break_entrance_and_exit()` — removes top wall of `_cells[0][0]` and bottom wall of `_cells[-1][-1]`
  3. `_break_walls_r(i, j)` — randomised recursive backtracking to carve the maze (uses `random.seed` if provided)
  4. `_reset_cells_visited()` — clears `visited` flags before solving
  5. `solve()` / `_solve_r(i, j)` — depth-first search from top-left to bottom-right; returns `True` on success

**Indexing convention:** `_cells[i][j]` where `i` is the column (x) and `j` is the row (y). `num_cols` controls the x-dimension, `num_rows` the y-dimension.

**Headless mode:** passing `win=None` (default) to `Maze` and `Cell` skips all drawing and animation, enabling fast unit tests without a display.

## Deployment

- **Docker:** `docker compose up --build` — requires X11 forwarding (`xhost +local:docker` on Linux)
- **Executable:** `bash scripts/build_exe.sh` — PyInstaller bundles everything into `dist/maze-solver`
- **Release:** push a `v*` tag to trigger `.github/workflows/release.yml`, which builds binaries for Linux, Windows, and macOS and creates a GitHub Release
