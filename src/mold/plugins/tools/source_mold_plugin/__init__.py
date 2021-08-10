from mold import Tool, templates_from_directory, hook
from ...domains import python, module
from ...categories import source as source_category
from ...face.source import Accepts as SourceVars
from ...face.build import Accepts as BuildVars
from ..source_basic_py import tool as source
from ..setuptools import tool as setuptools


def accept_vars():
    SourceVars.source_import_lines.append(
        'from . import domain, category, interface, tool'
    )
    slug = hook.Provides.project_slug
    BuildVars.build_entry_points['mold.plugins'].append(f'{slug}_plugins = {slug}')


tool = Tool(
    module,
    'Mold plugin',
    'create your own Mold plugin',
    depends=[source, setuptools],
    category=source_category,
    templates=templates_from_directory(__file__),
)
python.add_tool(tool)
