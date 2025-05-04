"""Main program."""

from maze_solver_with_python.core.models import Window


def main() -> None:
    """Main app."""
    win = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    main()
