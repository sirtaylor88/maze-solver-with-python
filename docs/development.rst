Development
===========

Prerequisites
-------------

- Python 3.12 (via `pyenv <https://github.com/pyenv/pyenv>`_)
- `uv <https://docs.astral.sh/uv/>`_ — fast Python package and project manager

Setup
-----

.. code-block:: bash

   pyenv local 3.12.9
   uv sync --all-groups
   uv run pre-commit install

`pre-commit <https://pre-commit.com/>`_ hooks run
`Ruff <https://docs.astral.sh/ruff/>`_,
`Pylint <https://pylint.readthedocs.io/>`_,
`Mypy <https://mypy.readthedocs.io/>`_,
`Bandit <https://bandit.readthedocs.io/>`_, and
`pydocstyle <https://www.pydocstyle.org/>`_
automatically on every commit.

Testing
-------

Run the full test suite with coverage:

.. code-block:: bash

   uv run pytest -vvs --cov=maze_solver_with_python maze_solver_with_python/tests/

Run a single test:

.. code-block:: bash

   uv run pytest -vvs maze_solver_with_python/tests/test_maze.py::test_maze_solve_returns_true

See the `pytest documentation <https://docs.pytest.org/>`_ and
`pytest-cov <https://pytest-cov.readthedocs.io/>`_ for more options.

Linting and type checking
-------------------------

.. code-block:: bash

   uv run ruff check --fix .       # lint + auto-fix (https://docs.astral.sh/ruff/)
   uv run ruff format .            # format
   uv run pylint maze_solver_with_python/
   uv run mypy .                   # https://mypy.readthedocs.io/
   uv run bandit -r . -c pyproject.toml  # security (https://bandit.readthedocs.io/)

Run all checks at once via `pre-commit <https://pre-commit.com/>`_:

.. code-block:: bash

   pre-commit run --all-files

Building the documentation
--------------------------

Docstrings follow the
`Google style guide <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_
and are rendered by `Sphinx <https://www.sphinx-doc.org/>`_ with the
`Napoleon <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_ extension.

Build once:

.. code-block:: bash

   uv run sphinx-build -b html docs/ docs/_build/html

Live-reload while editing (via
`sphinx-autobuild <https://github.com/sphinx-doc/sphinx-autobuild>`_):

.. code-block:: bash

   uv run sphinx-autobuild docs/ docs/_build/html

Building the standalone executable
-----------------------------------

Uses `PyInstaller <https://pyinstaller.org/>`_ to produce a single self-contained binary:

.. code-block:: bash

   bash scripts/build_exe.sh

Output: ``dist/maze-solver`` (Linux / macOS) or ``dist/maze-solver.exe`` (Windows).

CI / GitHub Actions
-------------------

The workflow
`release.yml <https://github.com/sirtaylor88/maze-solver-with-python/blob/main/.github/workflows/release.yml>`_
triggers on any ``v*`` tag push and on manual dispatch
(`workflow_dispatch <https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_dispatch>`_).

It builds the executable in parallel on three
`GitHub-hosted runners <https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners>`_:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Runner
     - Platform
     - Binary name
   * - ``ubuntu-latest``
     - Linux x86-64
     - ``maze-solver-linux-x86_64``
   * - ``windows-latest``
     - Windows x86-64
     - ``maze-solver-windows-x86_64.exe``
   * - ``macos-latest``
     - macOS ARM64
     - ``maze-solver-macos-arm64``

Once all three builds succeed, a
`GitHub Release <https://github.com/sirtaylor88/maze-solver-with-python/releases>`_
is created automatically with all binaries attached and auto-generated release notes.

To publish a release:

.. code-block:: bash

   git tag v1.0.0
   git push origin v1.0.0
