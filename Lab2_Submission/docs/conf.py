# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# Add these lines if they are not already in conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Adjust this if your module directory is different

extensions = [
    'sphinx.ext.autodoc',  # Essential for automodule
    'sphinx.ext.napoleon',  # Supports Google style docstrings
    'sphinx.ext.viewcode',  # Adds links to the highlighted source code
]

html_theme = 'sphinx_rtd_theme'  # Use the Read the Docs theme


project = 'lab3_oopGUI'
copyright = '2024, Ismail Allouch'
author = 'Ismail Allouch'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration



templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
