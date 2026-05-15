"""Render a solved maze to assets/maze_preview.png without a display."""

from pathlib import Path

from PIL import Image, ImageDraw

from maze_solver_with_python.core.models import Cell, Maze, Point

# ── Layout constants ──────────────────────────────────────────────────────────
ROWS, COLS = 14, 18
CELL = 40  # pixels per cell
MARGIN = 20  # outer padding
WALL = 3  # wall stroke width
BG = (255, 255, 255)
WALL_COLOR = (30, 30, 30)
PATH_COLOR = (220, 50, 50)  # red — active solution
UNDO_COLOR = (180, 180, 180)  # grey — backtracked

WIDTH = MARGIN * 2 + COLS * CELL
HEIGHT = MARGIN * 2 + ROWS * CELL


def _cell_rect(cell: Cell) -> tuple[int, int, int, int]:
    """Return the pixel bounding box (x1, y1, x2, y2) of *cell*."""
    return cell._x1, cell._y1, cell._x2, cell._y2


def draw_maze(draw: ImageDraw.ImageDraw, maze: Maze) -> None:
    """Draw all cell walls onto *draw*."""
    for col in maze._cells:
        for cell in col:
            x1, y1, x2, y2 = _cell_rect(cell)
            if cell.configs["top"]:
                draw.line([(x1, y1), (x2, y1)], fill=WALL_COLOR, width=WALL)
            if cell.configs["bottom"]:
                draw.line([(x1, y2), (x2, y2)], fill=WALL_COLOR, width=WALL)
            if cell.configs["left"]:
                draw.line([(x1, y1), (x1, y2)], fill=WALL_COLOR, width=WALL)
            if cell.configs["right"]:
                draw.line([(x2, y1), (x2, y2)], fill=WALL_COLOR, width=WALL)


def collect_path(maze: Maze) -> list[tuple[tuple[int, int], tuple[int, int], bool]]:
    """Re-run DFS and collect every draw_move call as (center_a, center_b, undo)."""
    moves: list[tuple[tuple[int, int], tuple[int, int], bool]] = []

    def _solve(i: int, j: int) -> bool:
        cell = maze._cells[i][j]
        cell.visited = True
        broken = [k for k, v in cell.configs.items() if not v]
        if cell == maze._cells[-1][-1]:
            return True
        neighbors = maze.get_neighbors_coords(i, j)
        eligible = [
            k
            for k, v in {
                k: maze._cells[x][y] for k, (x, y) in neighbors.items()
            }.items()
            if not v.visited and k in broken
        ]
        for direction in eligible:
            nx, ny = neighbors[direction]
            nxt = maze._cells[nx][ny]
            ca = (cell.center.x, cell.center.y)
            cb = (nxt.center.x, nxt.center.y)
            moves.append((ca, cb, False))
            if _solve(nx, ny):
                return True
            moves.append((ca, cb, True))
        return False

    maze._reset_cells_visited()
    _solve(0, 0)
    maze._reset_cells_visited()
    return moves


def draw_path(
    draw: ImageDraw.ImageDraw,
    moves: list[tuple[tuple[int, int], tuple[int, int], bool]],
) -> None:
    """Draw solution and backtrack segments onto *draw*."""
    r = CELL // 6  # dot radius at waypoints
    for (ax, ay), (bx, by), undo in moves:
        color = UNDO_COLOR if undo else PATH_COLOR
        draw.line([(ax, ay), (bx, by)], fill=color, width=WALL + 1)
    # Final pass: draw dots only on the winning path
    winning: set[tuple[int, int]] = set()
    stack: list[tuple[int, int]] = []
    for (ax, ay), (bx, by), undo in moves:
        if not undo:
            stack.append((bx, by))
            winning.add((ax, ay))
            winning.add((bx, by))
        elif stack:
            pt = stack.pop()
            winning.discard(pt)
    for x, y in winning:
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=PATH_COLOR)


def main() -> None:
    """Generate and save the maze preview image."""
    origin = Point(MARGIN, MARGIN)
    maze = Maze(origin, ROWS, COLS, CELL, CELL, win=None, seed=42)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw_maze(draw, maze)
    moves = collect_path(maze)
    draw_path(draw, moves)

    out = Path(__file__).resolve().parents[1] / "assets" / "maze_preview.png"
    img.save(out)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
