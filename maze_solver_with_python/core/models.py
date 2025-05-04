"""Module defining maze models."""

from tkinter import BOTH, Canvas, Tk


class Window:
    """Define a game window."""

    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("The Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self) -> None:
        """Redraw the window."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Wait for window to close."""
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def close(self) -> None:
        """Close the window."""
        self.__running = False
