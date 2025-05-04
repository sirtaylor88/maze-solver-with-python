"""Main program."""

from maze_solver_with_python.core.models import Maze, Point, Window


def main() -> None:
    """Main app."""
    win = Window(800, 600)
    p1 = Point(100, 100)

    Maze(p1, 10, 10, 20, 20, win)

    win.wait_for_close()


if __name__ == "__main__":
    main()
