"""Module defining maze models."""

import random
import time
from tkinter import BOTH, Canvas, Tk
from typing import Optional, Self


class Point:
    """A 2D coordinate point.

    Attributes:
        x (int): Horizontal position in pixels.
        y (int): Vertical position in pixels.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a Point.

        Args:
            x (int): Horizontal position in pixels.
            y (int): Vertical position in pixels.
        """
        self.x = x
        self.y = y


class Line:
    """A line segment between two points.

    Attributes:
        p1 (Point): Start point.
        p2 (Point): End point.
    """

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initialize a Line.

        Args:
            p1 (Point): Start point.
            p2 (Point): End point.
        """
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        """Draw the line onto a tkinter canvas.

        Args:
            canvas (Canvas): The tkinter ``Canvas`` to draw on.
            fill_color (str): Color of the line. Defaults to ``"black"``.
        """
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Window:
    """A tkinter application window for rendering the maze.

    Wraps a ``Tk`` root and a ``Canvas`` widget. Pass ``win=None`` to
    :class:`Maze` or :class:`Cell` to run headlessly (useful for tests).
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize the Window.

        Args:
            width (int): Width of the canvas in pixels.
            height (int): Height of the canvas in pixels.
        """
        self.__root = Tk()
        self.__root.title("The Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self) -> None:
        """Process all pending tkinter events and redraw the window."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Block until the window is closed by the user."""
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def close(self) -> None:
        """Signal the window to stop its event loop."""
        self.__running = False

    def draw_line(
        self, line: Line, fill_color: str = "black", visible: bool = True
    ) -> None:
        """Draw a line on the canvas.

        Args:
            line (Line): The :class:`Line` to draw.
            fill_color (str): Color when the line is visible. Defaults to
                ``"black"``.
            visible (bool): When ``False`` the line is drawn white, effectively
                erasing it.
        """
        if not visible:
            fill_color = "white"
        line.draw(self.__canvas, fill_color)


class Cell:
    """A single rectangular cell within the maze grid.

    Each cell tracks whether its four walls are present and whether it has
    been visited by the generation or solving algorithm.

    Attributes:
        configs (dict[str, bool]): Wall-presence flags keyed by ``"top"``,
            ``"bottom"``, ``"left"``, and ``"right"`` (``True`` = wall
            present).
        visited (bool): ``True`` once the cell has been visited by DFS.
    """

    def __init__(
        self,
        top_left: Point,
        right_bottom: Point,
        win: Optional[Window] = None,
        **kwargs: bool,
    ) -> None:
        """Initialize a Cell.

        Args:
            top_left (Point): Top-left corner of the cell in pixels.
            right_bottom (Point): Bottom-right corner of the cell in pixels.
            win (Window | None): Window used for rendering. Pass ``None`` to
                skip drawing.
            **kwargs (bool): Optional wall overrides — accepted keys:
                ``left``, ``right``, ``top``, ``bottom`` (default ``True``).
        """
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
        """Render the cell's walls onto the window canvas.

        Walls flagged ``False`` in :attr:`configs` are drawn white (erasing
        them visually). Does nothing when ``win`` is ``None``.
        """
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
        """The center point of the cell in pixels.

        Returns:
            Point: The midpoint between ``top_left`` and ``right_bottom``.
        """
        return Point(
            int((self._x2 + self._x1) / 2),
            int((self._y2 + self._y1) / 2),
        )

    def draw_move(self, to_cell: Self, undo: bool = False) -> None:
        """Draw a path segment from this cell's center to an adjacent cell's center.

        Args:
            to_cell (Cell): The neighbouring :class:`Cell` to draw a line
                toward.
            undo (bool): When ``True`` the line is drawn grey to mark a
                backtracked path. Defaults to ``False`` (red).
        """
        if self._w is None:
            return

        fill_color = "red"
        if undo:
            fill_color = "grey"

        self._w.draw_line(Line(self.center, to_cell.center), fill_color)


class Maze:
    """A randomly generated, solvable rectangular maze.

    The maze is stored as a column-major 2-D list of :class:`Cell` objects:
    ``_cells[col][row]``, where *col* indexes the x-axis and *row* the y-axis.

    Generation uses randomised recursive backtracking (DFS). Solving uses a
    depth-first search from the top-left entrance ``(0, 0)`` to the
    bottom-right exit ``(num_cols-1, num_rows-1)``.

    Attributes:
        top_left (Point): Pixel offset of the maze's top-left corner.
        num_rows (int): Number of rows (y-axis).
        num_cols (int): Number of columns (x-axis).
        cell_size_x (int): Width of each cell in pixels.
        cell_size_y (int): Height of each cell in pixels.
        win (Window | None): Rendering window (``None`` for headless mode).
    """

    def __init__(
        self,
        top_left: Point,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Optional[Window] = None,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize and fully generate the maze.

        Runs the complete generation pipeline: create cells, open the
        entrance and exit, carve passages, reset visited flags.

        Args:
            top_left (Point): Pixel coordinate of the top-left corner of the
                maze.
            num_rows (int): Number of rows.
            num_cols (int): Number of columns.
            cell_size_x (int): Width of each cell in pixels.
            cell_size_y (int): Height of each cell in pixels.
            win (Window | None): Window for rendering. Pass ``None`` to run
                headlessly.
            seed (int | None): Optional RNG seed for reproducible maze
                layouts.
        """
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

    def _create_cells(self) -> None:
        """Populate ``_cells`` with a grid of :class:`Cell` objects and draw them.

        ``_cells`` is column-major: ``_cells[i]`` is the list of cells in
        column *i*, ordered top to bottom.
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
        """Draw cell ``(i, j)`` and trigger an animation frame.

        Args:
            i (int): Column index.
            j (int): Row index.
        """
        self._cells[i][j].draw()
        self._animate()

    def _animate(self) -> None:
        """Redraw the window and pause briefly to visualise progress.

        Does nothing when ``win`` is ``None`` (headless mode).
        """
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        """Open the maze entrance and exit.

        Removes the top wall of ``_cells[0][0]`` (entrance) and the bottom
        wall of ``_cells[-1][-1]`` (exit).
        """
        top_left_cell = self._cells[0][0]
        right_bottom_cell = self._cells[-1][-1]

        top_left_cell.configs["top"] = False
        right_bottom_cell.configs["bottom"] = False

        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def get_neighbors_coords(self, i: int, j: int) -> dict[str, tuple[int, int]]:
        """Return in-bounds neighbours of cell ``(i, j)``.

        Args:
            i (int): Column index of the current cell.
            j (int): Row index of the current cell.

        Returns:
            dict[str, tuple[int, int]]: A dict mapping direction strings
            (``"top"``, ``"bottom"``, ``"left"``, ``"right"``) to
            ``(col, row)`` index tuples for each valid in-bounds neighbour.
        """
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
        """Return the direction opposite to *direction*.

        Args:
            direction (str): One of ``"top"``, ``"bottom"``, ``"left"``,
                ``"right"``.

        Returns:
            str: The opposite direction string.

        Raises:
            ValueError: If *direction* is not a recognised value.
        """
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
        """Carve passages using randomised recursive backtracking.

        Marks the current cell visited and randomly removes shared walls
        between it and an unvisited neighbour, then recurses into that
        neighbour until all cells are visited.

        Args:
            i (int): Column index of the current cell.
            j (int): Row index of the current cell.
        """
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
        """Clear the ``visited`` flag on every cell in the grid."""
        for i in range(self.num_cols):  # x-axis
            for j in range(self.num_rows):  # y-axis
                self._cells[i][j].visited = False

    def _solve_r(self, i: int, j: int) -> bool:
        """Depth-first search from cell ``(i, j)`` toward the exit.

        Moves only through broken walls and unvisited cells. Draws the active
        path in red and backtracks in grey on dead ends.

        Args:
            i (int): Column index of the current cell.
            j (int): Row index of the current cell.

        Returns:
            bool: ``True`` if a path to the exit was found, ``False``
            otherwise.
        """
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
        """Solve the maze using depth-first search.

        Returns:
            bool: ``True`` if the maze has a solution, ``False`` if it is
            unsolvable.
        """
        return self._solve_r(0, 0)
