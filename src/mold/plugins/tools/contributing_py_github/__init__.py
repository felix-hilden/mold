from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.todo import Accepts as TodoVars
from ..pytest_tox import tool as tests
from ..github import tool as github


def accept_vars():
    TodoVars.todo_items.append('read ``contributing.rst`` for setup instructions')


tool = Tool(
    module,
    'contributing Python+GitHub',
    'contributing guide for Python projects using GitHub',
    depends=[tests, github],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
