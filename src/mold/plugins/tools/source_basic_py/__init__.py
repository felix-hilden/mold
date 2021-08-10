from mold import Tool, templates_from_directory, hook
from ...domains import python, module
from ...face.source import interface as source
from ...face.readme import interface as readme, Accepts as ReadmeVars

example = """\
.. code:: python

   import {slug}

   print({slug}.__version__)\
"""


def accept_vars():
    lines = example.format(slug=hook.Provides.project_slug).split('\n')
    ReadmeVars.readme_example_lines = lines


tool = Tool(
    module,
    'python module',
    'basic Python source module template',
    depends=[source, readme],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
