#!/usr/bin/env bash
set -euo pipefail

uv run pyinstaller \
    --onefile \
    --name maze-solver \
    --clean \
    --noconfirm \
    maze_solver_with_python/__main__.py

echo "Executable ready: dist/maze-solver"
