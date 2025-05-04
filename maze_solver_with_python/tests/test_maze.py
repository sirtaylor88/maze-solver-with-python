"""Unit tests for maze."""

from maze_solver_with_python.core.models import Maze, Point


def test_maze() -> None:
    """Test that maze is generated correctly."""
    m = Maze(Point(100, 100), 10, 10, 20, 20)

    assert len(m._cells) == 10
    assert len(m._cells[0]) == 10
    assert m._cells[0][0].configs["has_top_wall"] is False
    assert m._cells[-1][-1].configs["has_bottom_wall"] is False
