"""Main program."""

from maze_solver_with_python.core.models import Maze, Point, Window


def main() -> None:
    """Main app."""
    win = Window(800, 600)
    p1 = Point(50, 50)

    m = Maze(p1, 10, 14, 50, 50, win)
    m.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
