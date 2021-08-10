from mold import Tool, templates_from_directory
from ...domains import python, module
from ...categories import gitignore as gitignore_category
from ...face.gitignore import interface as gitignore
from ...face.todo import Accepts as TodoVars


def accept_vars() -> None:
    TodoVars.todo_items.append(
        'for more potential ``.gitignore`` targets see '
        '`https://github.com/github/gitignore/blob/master/Python.gitignore`_'
    )


tool = Tool(
    module,
    'minimal gitignore',
    'git version control with minimal gitignore file',
    depends=[gitignore],
    category=gitignore_category,
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
