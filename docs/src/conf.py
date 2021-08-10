import os
import sys
from pathlib import Path

conf_dir = Path(os.path.realpath(__file__)).parent
root = conf_dir.parent.parent / 'src'
sys.path.insert(0, str(root))

project = 'mold'
author = 'Felix Hildén'
copyright = '2021, Felix Hildén'
release = Path(root, 'mold', 'VERSION').read_text().strip()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

master_doc = 'index'
exclude_patterns = ['build']
html_theme = 'sphinx_rtd_theme'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
}

# Create CLI reference
from mold.cli import mold_help
from textwrap import indent

cli_rst = """
.. _cli:

Command line reference
======================

.. code-block:: text

""" + indent(mold_help, '   ') + '\n'
cli_file = conf_dir / 'command_line_reference.rst'
cli_file.write_text(cli_rst)

# Create plugin documentation
from mold.doc import render_docs

domains = ['python']
tools = [
    'contributing_py_github',
    'github',
    'github_actions',
    'gitignore_minimal',
    'gitignore_python',
    'license_mit',
    'pytest_tox',
    'readme_pypi',
    'readme_rst',
    'rtd_sphinx',
    'setuptools',
    'source_basic_py',
    'source_cli_py',
    'source_mold_plugin',
    'sphinx',
    'todo_rst',
]
categories = ['gitignore', 'license_', 'source']
interfaces = [
    'build',
    'doc',
    'doc_host',
    'github',
    'gitignore',
    'license',
    'package_readme',
    'read_the_docs',
    'readme',
    'source',
    'todo',
    'vcs_host',
]

plugins_text = render_docs(
    'Builtin Mold plugins.',
    domain_locations=['mold.plugins.domains.' + domain for domain in domains],
    tool_locations=[f'mold.plugins.tools.{tool}.tool' for tool in tools],
    category_locations=['mold.plugins.categories.' + cat for cat in categories],
    interface_locations=[f'mold.plugins.face.{face}.interface' for face in interfaces],
)
plugins_path = conf_dir / 'plugins.rst'
plugins_path.write_text(plugins_text)
