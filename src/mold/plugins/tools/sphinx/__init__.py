"""
Provides an extra question and configuration ``docs_semver_over_calver``
to :mod:`doc` to determine whether Semantic or Calendar Versioning is wanted.
"""
from mold import Tool, Question, templates_from_directory
from ...domains import python, module
from ...face.doc import interface as doc, Provides as DocVars
from ...face.readme import interface as readme
from ...face.source import interface as source
from ...face.license import interface as license_
from ...face.build import Accepts as BuildVars
from ...face.gitignore import Accepts as IgnoreVars
from ..setuptools import tool as setuptools

_version_msg = """\
Choose a versioning scheme:
Semantic Versioning (e.g. 1.7.2) or Calendar (e.g. 2018.11.03) Versioning
[S]/C (leave empty for Semantic Versioning)\
"""

questions = [
    Question('docs_semver_over_calver', _version_msg)
]
doc.questions.extend(questions)


def provide_vars():
    DocVars.docs_semver_over_calver = questions[0].response.lower() != 'c'


def accept_vars():
    IgnoreVars.gitignore_items.append('/docs/build/')
    BuildVars.build_extra_deps['docs'].extend([
        'sphinx',
        'sphinx-rtd-theme',
    ])
    BuildVars.build_manifest_in_items = getattr(
        BuildVars, 'build_manifest_in_items', []
    )
    BuildVars.build_manifest_in_items.extend([
        'graft docs',
        'prune docs/build',
    ])


tool = Tool(
    module,
    'sphinx',
    'Sphinx documentation with initial structure and release notes',
    depends=[doc, readme, source, setuptools, license_],
    templates=templates_from_directory(__file__),
    provide_vars=provide_vars,
    accept_vars=accept_vars,
)
python.add_tool(tool)
