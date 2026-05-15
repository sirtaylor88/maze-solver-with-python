"""Unit tests for maze models."""

import pytest

from maze_solver_with_python.core.models import Cell, Maze, Point

# ---------------------------------------------------------------------------
# Point
# ---------------------------------------------------------------------------


def test_point_attributes() -> None:
    """Point stores x and y coordinates."""
    p = Point(3, 7)
    assert p.x == 3
    assert p.y == 7


# ---------------------------------------------------------------------------
# Cell
# ---------------------------------------------------------------------------


def test_cell_default_walls() -> None:
    """All four walls are present by default."""
    cell = Cell(Point(0, 0), Point(10, 10))
    assert cell.configs == {"left": True, "right": True, "top": True, "bottom": True}


def test_cell_wall_override() -> None:
    """Wall kwargs override the defaults."""
    cell = Cell(Point(0, 0), Point(10, 10), left=False, bottom=False)
    assert cell.configs["left"] is False
    assert cell.configs["bottom"] is False
    assert cell.configs["top"] is True
    assert cell.configs["right"] is True


def test_cell_not_visited_by_default() -> None:
    """Cells start unvisited."""
    cell = Cell(Point(0, 0), Point(10, 10))
    assert cell.visited is False


def test_cell_center_even() -> None:
    """Center is the midpoint of the bounding box (even dimensions)."""
    cell = Cell(Point(0, 0), Point(20, 20))
    c = cell.center
    assert c.x == 10
    assert c.y == 10


def test_cell_center_odd() -> None:
    """Center is truncated toward zero for odd cell sizes."""
    cell = Cell(Point(0, 0), Point(15, 15))
    c = cell.center
    assert c.x == 7
    assert c.y == 7


def test_cell_repr() -> None:
    """__repr__ includes the corner coordinates."""
    cell = Cell(Point(5, 10), Point(25, 30))
    assert "5" in repr(cell)
    assert "30" in repr(cell)


# ---------------------------------------------------------------------------
# Maze – grid dimensions
# ---------------------------------------------------------------------------


def test_maze_grid_dimensions() -> None:
    """_cells has the correct number of columns and rows."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=8, cell_size_x=10, cell_size_y=10)
    assert len(m._cells) == 8
    assert all(len(col) == 5 for col in m._cells)


def test_maze_square_grid() -> None:
    """Square maze has equal columns and rows."""
    m = Maze(Point(0, 0), num_rows=4, num_cols=4, cell_size_x=20, cell_size_y=20)
    assert len(m._cells) == 4
    assert len(m._cells[0]) == 4


# ---------------------------------------------------------------------------
# Maze – entrance and exit
# ---------------------------------------------------------------------------


def test_maze_entrance_top_wall_removed() -> None:
    """Top wall of the entrance cell (0, 0) is removed."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    assert m._cells[0][0].configs["top"] is False


def test_maze_exit_bottom_wall_removed() -> None:
    """Bottom wall of the exit cell (last col, last row) is removed."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    assert m._cells[-1][-1].configs["bottom"] is False


def test_maze_entrance_other_walls_intact() -> None:
    """Only the top wall of the entrance is removed; others start intact."""
    m = Maze(Point(0, 0), num_rows=3, num_cols=3, cell_size_x=10, cell_size_y=10)
    assert m._cells[0][0].configs["left"] is True


# ---------------------------------------------------------------------------
# Maze – visited reset
# ---------------------------------------------------------------------------


def test_maze_all_cells_not_visited_after_init() -> None:
    """All cells are unvisited after construction."""
    m = Maze(Point(0, 0), num_rows=4, num_cols=4, cell_size_x=10, cell_size_y=10)
    for col in m._cells:
        for cell in col:
            assert cell.visited is False


# ---------------------------------------------------------------------------
# Maze – neighbour lookup
# ---------------------------------------------------------------------------


def test_get_neighbors_coords_center() -> None:
    """A centre cell has all four neighbours."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    neighbors = m.get_neighbors_coords(2, 2)
    assert set(neighbors.keys()) == {"top", "bottom", "left", "right"}


def test_get_neighbors_coords_top_left_corner() -> None:
    """The top-left corner cell has only bottom and right neighbours."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    neighbors = m.get_neighbors_coords(0, 0)
    assert set(neighbors.keys()) == {"bottom", "right"}


def test_get_neighbors_coords_bottom_right_corner() -> None:
    """The bottom-right corner cell has only top and left neighbours."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    neighbors = m.get_neighbors_coords(4, 4)
    assert set(neighbors.keys()) == {"top", "left"}


def test_get_neighbors_coords_values() -> None:
    """Neighbour coords are offset correctly from (i, j)."""
    m = Maze(Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    neighbors = m.get_neighbors_coords(2, 2)
    assert neighbors["top"] == (2, 1)
    assert neighbors["bottom"] == (2, 3)
    assert neighbors["left"] == (1, 2)
    assert neighbors["right"] == (3, 2)


# ---------------------------------------------------------------------------
# Maze – opposite direction
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "direction, expected",
    [
        ("top", "bottom"),
        ("bottom", "top"),
        ("left", "right"),
        ("right", "left"),
    ],
)
def test_get_opposite_direction(direction: str, expected: str) -> None:
    """get_opposite_direction returns the correct opposite."""
    assert Maze.get_opposite_direction(direction) == expected


def test_get_opposite_direction_invalid() -> None:
    """get_opposite_direction raises ValueError for unknown directions."""
    with pytest.raises(ValueError, match="Unknown direction"):
        Maze.get_opposite_direction("diagonal")


# ---------------------------------------------------------------------------
# Maze – solve
# ---------------------------------------------------------------------------


def test_maze_solve_returns_true() -> None:
    """Every valid maze generated by the algorithm is solvable."""
    m = Maze(
        Point(0, 0), num_rows=6, num_cols=6, cell_size_x=10, cell_size_y=10, seed=42
    )
    assert m.solve() is True


def test_maze_solve_1x1() -> None:
    """A 1×1 maze is trivially solved (start == exit)."""
    m = Maze(Point(0, 0), num_rows=1, num_cols=1, cell_size_x=10, cell_size_y=10)
    assert m.solve() is True


def test_maze_solve_reproducible_with_seed() -> None:
    """Two mazes with the same seed produce the same solution outcome."""
    m1 = Maze(
        Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10, seed=7
    )
    m2 = Maze(
        Point(0, 0), num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10, seed=7
    )
    assert m1.solve() == m2.solve()
