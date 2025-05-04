"""Main program."""

from maze_solver_with_python.core.models import Cell, Point, Window


def main() -> None:
    """Main app."""
    win = Window(800, 600)
    p1 = Point(100, 100)
    p2 = Point(200, 200)

    cell1 = Cell(win, p1, p2, has_right_wall=False)
    cell1.draw()

    p3 = Point(200, 100)
    p4 = Point(300, 200)
    cell2 = Cell(win, p3, p4, has_left_wall=False, has_right_wall=False)
    cell2.draw()

    cell1.draw_move(cell2)

    win.wait_for_close()


if __name__ == "__main__":
    main()
