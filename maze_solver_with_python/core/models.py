"""Module defining maze models."""

import typing as tp
from tkinter import BOTH, Canvas, Tk


class Point:
    """Define a Point."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    """Define a Line."""

    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        """Draw a line."""
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


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

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """Draw a line in window canvas."""
        line.draw(self.__canvas, fill_color)


class Cell:
    """Define a cell."""

    def __init__(
        self,
        w: Window,
        top_left: Point,
        right_bottom: Point,
        **kwargs: bool,
    ) -> None:
        self.configs = {}
        self.configs["has_left_wall"] = kwargs.pop("has_left_wall", True)
        self.configs["has_right_wall"] = kwargs.pop("has_right_wall", True)
        self.configs["has_top_wall"] = kwargs.pop("has_top_wall", True)
        self.configs["has_bottom_wall"] = kwargs.pop("has_bottom_wall", True)

        self._x1 = top_left.x
        self._y1 = top_left.y
        self._x2 = right_bottom.x
        self._y2 = right_bottom.y

        self._w = w

    def draw(self) -> None:
        """Draw a cell."""
        if self.configs["has_left_wall"]:
            self._w.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            )

        if self.configs["has_right_wall"]:
            self._w.draw_line(
                Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            )

        if self.configs["has_top_wall"]:
            self._w.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            )

        if self.configs["has_bottom_wall"]:
            self._w.draw_line(
                Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            )

    @property
    def center(self) -> Point:
        """Return the center point of the cell."""
        return Point(
            int((self._x2 + self._x1) / 2),
            int((self._y2 + self._y1) / 2),
        )

    def draw_move(self, to_cell: tp.Self, undo: bool = False) -> None:
        """Draw a move."""
        fill_color = "red"
        if undo:
            fill_color = "grey"

        self._w.draw_line(Line(self.center, to_cell.center), fill_color)
