# pylint: disable=invalid-name
"""Sphinx configuration for Maze Solver with Python."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# -- Project information -----------------------------------------------------

project = "Maze Solver with Python"
author = "Nhat Tai NGUYEN"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Napoleon — Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_attr_annotations = True

# Autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# Intersphinx — link to Python stdlib
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build"]

# -- HTML output -------------------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]
html_theme_options = {
    "description": "A maze generator and solver built with Python and tkinter.",
    "github_user": "sirtaylor88",
    "github_repo": "maze-solver-with-python",
    "github_button": True,
    "github_type": "star",
    "fixed_sidebar": True,
}
