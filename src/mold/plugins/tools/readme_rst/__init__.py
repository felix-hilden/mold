from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.readme import interface as readme

tool = Tool(
    module,
    'rst readme',
    'basic RST readme file',
    depends=[readme],
    templates=templates_from_directory(__file__),
)
python.add_tool(tool)
