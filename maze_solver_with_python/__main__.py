"""Main program."""

from maze_solver_with_python.core.models import Line, Point, Window


def main() -> None:
    """Main app."""
    win = Window(800, 600)
    p1 = Point(100, 100)
    p2 = Point(200, 200)

    win.draw_line(Line(p1, p2), "red")
    win.wait_for_close()


if __name__ == "__main__":
    main()
