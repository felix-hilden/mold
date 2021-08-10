from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.todo import interface as todo

tool = Tool(
    module,
    'rst todo',
    'basic RST TODO file',
    depends=[todo],
    templates=templates_from_directory(__file__),
)
python.add_tool(tool)
