Maze Solver with Python
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents

   api

A maze generator and solver built with Python and tkinter.

Mazes are generated with **randomised recursive backtracking** and solved with
**depth-first search**, animated in real time inside a tkinter window.

Quickstart
----------

.. code-block:: bash

   uv run maze

An 800 × 600 window opens. The maze is drawn cell by cell as it is generated,
then a red path traces the solution. Backtracked steps are shown in grey.

How it works
------------

The grid is stored as a column-major 2-D list of :class:`~maze_solver_with_python.core.models.Cell`
objects: ``_cells[col][row]``.

- **Entrance** — top wall of ``_cells[0][0]``
- **Exit** — bottom wall of ``_cells[-1][-1]``
- Pass a ``seed`` to :class:`~maze_solver_with_python.core.models.Maze` for reproducible layouts.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
