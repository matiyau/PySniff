# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pygit2 import Repository
# sys.path.insert(0, os.path.abspath('.'))

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(_SCRIPT_DIR, '../pysniff'))

# -- Project information -----------------------------------------------------

project = 'PySniff'
copyright = '2021, Koppány Cserna, Nishad Mandlik'
author = 'Koppány Cserna, Nishad Mandlik'


# -- General configuration ---------------------------------------------------

# Linking to Source Code
branch = Repository(os.path.join(_SCRIPT_DIR, "../")).head.shorthand


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://gitlab.ewi.tudelft.nl/et4394/2020-2021/wn-group-08/-/tree/" + branch + \
        "/pysniff/" + filename + ".py"


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.napoleon',
    'sphinx.ext.linkcode',
    'm2r2'
]
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = 'tudelft_logo.png'
html_favicon = 'tudelft_fav.ico'
html_theme_options = {
    'style_nav_header_background': '#009ce3',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
