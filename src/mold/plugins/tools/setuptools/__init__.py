"""
Accepts an additional variable "build_manifest_in_items" (List[str])
to include project files in the sdist build.
"""
from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.build import interface as build, Accepts
from ...face.readme import interface as readme
from ...face.source import interface as source, Accepts as SourceVars
from ...face.todo import interface as todo, Accepts as TodoVars
from ...face.gitignore import Accepts as GitignoreVars


def accept_vars():
    Accepts.build_extra_deps['build'].extend(['build', 'twine'])

    TodoVars.todo_items.append('fill in package metadata in ``setup.py``')
    GitignoreVars.gitignore_items.extend([
        '/build/',
        '/dist/',
        '/*.egg-info/',
    ])
    SourceVars.source_import_lines.extend([
        'import os as _os',
        'from pathlib import Path as _Path',
    ])
    SourceVars.source_code_lines.extend([
        '_version_file = _Path(_os.path.realpath(__file__)).parent / "VERSION"',
        '__version__ = _version_file.read_text().strip()',
    ])


def handle_accept():
    Accepts.build_manifest_in_items = getattr(Accepts, 'build_manifest_in_items', [])
    Accepts.build_manifest_in_items.append(
        'include ' + (Accepts.build_readme_file or 'readme.rst')
    )


tool = Tool(
    module,
    'setuptools',
    'setuptools build and dependencies for source and wheel distributions',
    depends=[readme, build, source, todo],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
    handle_accept=handle_accept,
)
python.add_tool(tool)
