from mold import Tool, templates_from_directory, hook
from ...domains import python, module
from ...categories import source as source_category
from ...face.build import Accepts as BuildVars
from ...face.readme import interface as readme, Accepts as ReadmeVars
from ..source_basic_py import tool as source

example = """\
.. code: sh

   $ {slug} arg --flag --opt value
   $ {slug} --help\
"""


def accept_vars():
    slug = hook.Provides.project_slug
    ReadmeVars.readme_example_lines = example.format(slug=slug).split('\n')
    BuildVars.build_entry_points['console_scripts'].append(f'{slug} = {slug}.cli:main')


tool = Tool(
    module,
    'python cli',
    'source for a Python CLI tool',
    depends=[source, readme],
    category=source_category,
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
