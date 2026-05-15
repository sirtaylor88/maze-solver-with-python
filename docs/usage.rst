Usage
=====

Running locally
---------------

.. code-block:: bash

   uv run maze

An 800 × 600 window opens. The maze is drawn cell by cell as it is generated,
then a red path traces the solution. Backtracked steps are shown in grey.

Docker
------

The container forwards the GUI to your host display via
`X11 <https://www.x.org/wiki/>`_. The image is built with a
`multi-stage Dockerfile <https://docs.docker.com/build/building/multi-stage/>`_:
a builder stage installs dependencies with `uv <https://docs.astral.sh/uv/>`_,
and a slim runtime stage adds the
`Tcl/Tk <https://www.tcl.tk/>`_ libraries required by tkinter.

**Prerequisites:** `Docker <https://docs.docker.com/get-started/>`_ and a
running X11 server. On Linux, grant the container access first:

.. code-block:: bash

   xhost +local:docker

With Docker Compose
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   docker compose up --build

See the `Docker Compose documentation <https://docs.docker.com/compose/>`_ for
additional options.

Manually
~~~~~~~~

.. code-block:: bash

   docker build -t maze-solver .

   docker run --rm \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     --network host \
     maze-solver

.. note::

   **WSL2:** `WSLg <https://github.com/microsoft/wslg>`_ provides X11
   automatically. Export ``DISPLAY=:0`` if the variable is not already set.

Standalone executable
---------------------

The executable is built with `PyInstaller <https://pyinstaller.org/>`_, which
bundles the interpreter and all dependencies — no Python installation is
required on the target machine. The output is platform-specific; build on the
OS you intend to run it on.

.. code-block:: bash

   bash scripts/build_exe.sh

The binary is written to ``dist/maze-solver`` (Linux / macOS) or
``dist/maze-solver.exe`` (Windows).

Pre-built binaries for Linux, Windows, and macOS are attached to every
`GitHub Release <https://github.com/sirtaylor88/maze-solver-with-python/releases>`_.
