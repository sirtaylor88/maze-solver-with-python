"""Module defining maze models."""

import random
import time
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

    def draw_line(
        self, line: Line, fill_color: str = "black", visible: bool = True
    ) -> None:
        """Draw a line in window canvas."""
        if not visible:
            fill_color = "white"
        line.draw(self.__canvas, fill_color)


class Cell:
    """Define a cell."""

    def __init__(
        self,
        top_left: Point,
        right_bottom: Point,
        win: tp.Optional[Window] = None,
        **kwargs: bool,
    ) -> None:
        self.configs = {}
        self.configs["left"] = kwargs.pop("left", True)
        self.configs["right"] = kwargs.pop("right", True)
        self.configs["top"] = kwargs.pop("top", True)
        self.configs["bottom"] = kwargs.pop("bottom", True)

        self._x1 = top_left.x
        self._y1 = top_left.y
        self._x2 = right_bottom.x
        self._y2 = right_bottom.y

        self._w = win
        self.visited = False

    def __repr__(self) -> str:
        return f"Cell [({self._x1}, {self._y1}), ({self._x2}, {self._y2})]"

    def draw(self) -> None:
        """Draw a cell."""

        if self._w is None:
            return

        # Left wall
        left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self._w.draw_line(left_wall, visible=self.configs["left"])

        # Right wall
        right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self._w.draw_line(right_wall, visible=self.configs["right"])

        # Top wall
        top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self._w.draw_line(top_wall, visible=self.configs["top"])

        # Bottom wall
        bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self._w.draw_line(bottom_wall, visible=self.configs["bottom"])

    @property
    def center(self) -> Point:
        """Return the center point of the cell."""
        return Point(
            int((self._x2 + self._x1) / 2),
            int((self._y2 + self._y1) / 2),
        )

    def draw_move(self, to_cell: tp.Self, undo: bool = False) -> None:
        """Draw a move."""

        if self._w is None:
            return

        fill_color = "red"
        if undo:
            fill_color = "grey"

        self._w.draw_line(Line(self.center, to_cell.center), fill_color)


class Maze:
    """Define a maze."""

    def __init__(
        self,
        top_left: Point,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: tp.Optional[Window] = None,
        seed: tp.Optional[int] = None,
    ):
        self.top_left = top_left

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

        self.win = win
        self._cells: list[list[Cell]] = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed is not None:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        """Fill the maze with cells.

        col[0]: [row 0, row 1, row 2]
        col[1]: [row 0, row 1, row 2]
        col[2]: [row 0, row 1, row 2]
        """

        for i in range(self.num_cols):  # x-axis
            col_cells = []
            for j in range(self.num_rows):  # y-axis
                top_left_of_cell = Point(
                    self.top_left.x + i * self.cell_size_x,
                    self.top_left.y + j * self.cell_size_y,
                )
                right_bottom_of_cell = Point(
                    self.top_left.x + (i + 1) * self.cell_size_x,
                    self.top_left.y + (j + 1) * self.cell_size_y,
                )
                cell = Cell(top_left_of_cell, right_bottom_of_cell, win=self.win)
                col_cells.append(cell)
            self._cells.append(col_cells)

        for i in range(self.num_cols):  # x-axis
            for j in range(self.num_rows):  # y-axis
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        """Draw the cell."""

        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        """Visualize the algorithm in real time."""

        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        """Breaking entrance and exit."""

        top_left_cell = self._cells[0][0]
        right_bottom_cell = self._cells[-1][-1]

        top_left_cell.configs["top"] = False
        right_bottom_cell.configs["bottom"] = False

        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def get_neighbors_coords(self, i: int, j: int) -> dict[str, tuple[int, int]]:
        """Get neighbors."""

        neighbors = {
            "top": (i, j - 1),
            "bottom": (i, j + 1),
            "left": (i - 1, j),
            "right": (i + 1, j),
        }

        for k, (x, y) in list(neighbors.items()):
            if not (0 <= x <= self.num_cols - 1 and 0 <= y <= self.num_rows - 1):
                del neighbors[k]
        return neighbors

    @staticmethod
    def get_opposite_direction(direction: str) -> str:
        """Return opposite direction."""
        match direction:
            case "top":
                return "bottom"
            case "bottom":
                return "top"
            case "left":
                return "right"
            case "right":
                return "left"
            case _:
                raise ValueError("Unknown direction.")

    def _break_walls_r(self, i: int, j: int) -> None:
        """Breaking walls."""

        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            neighbors_coords = self.get_neighbors_coords(i, j)
            neighbors = {k: self._cells[x][y] for k, (x, y) in neighbors_coords.items()}
            unvisited = [k for k, v in list(neighbors.items()) if not v.visited]

            if not unvisited:
                self._draw_cell(i, j)
                return

            direction = random.choice(unvisited)  # nosec

            current_cell.configs[direction] = False
            self._draw_cell(i, j)

            x, y = neighbors_coords[direction]
            next_cell = self._cells[x][y]
            next_cell.configs[self.get_opposite_direction(direction)] = False

            self._break_walls_r(x, y)

    def _reset_cells_visited(self) -> None:
        """Reset visited cells."""

        for i in range(self.num_cols):  # x-axis
            for j in range(self.num_rows):  # y-axis
                self._cells[i][j].visited = False

    def _solve_r(self, i: int, j: int) -> bool:
        """Solve the maze recursively."""
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True

        broken_walls = [k for k, v in current_cell.configs.items() if not v]

        if current_cell == self._cells[-1][-1]:
            return True

        neighbors_coords = self.get_neighbors_coords(i, j)
        neighbors = {k: self._cells[x][y] for k, (x, y) in neighbors_coords.items()}
        eligible_directions = [
            k for k, v in list(neighbors.items()) if not v.visited and k in broken_walls
        ]

        for direction in eligible_directions:
            x, y = neighbors_coords[direction]
            next_cell = self._cells[x][y]
            current_cell.draw_move(next_cell)
            if self._solve_r(x, y):
                return True
            current_cell.draw_move(next_cell, undo=True)

        return False

    def solve(self) -> bool:
        """Solve the maze."""
        return self._solve_r(0, 0)
