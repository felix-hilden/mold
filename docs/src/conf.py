import os
import sys
from pathlib import Path

_root = Path(os.path.realpath(__file__)).parent.parent.parent
sys.path.insert(0, _root)

project = 'mold'
author = 'Felix Hildén'
copyright = '2021, Felix Hildén'
release = Path(_root, 'mold', 'VERSION').read_text().strip()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

master_doc = 'index'
exclude_patterns = ['build']
autosummary_generate = True
html_theme = 'sphinx_rtd_theme'
