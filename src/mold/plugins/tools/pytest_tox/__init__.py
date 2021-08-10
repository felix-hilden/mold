from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.gitignore import Accepts as GitignoreVars
from ...face.source import Provides as SourceVars
from ...face.build import Accepts as BuildVars
from ..source_basic_py import tool as source
from ..setuptools import tool as build

pytest_toml = """
python_files = "*.py"
testpaths = ["tests"]
"""

coverage_run_toml = """
source = ["{source_dir}"]
branch = true
command_line = "-m pytest"
"""

coverage_report_toml = """
precision = 1
skip_covered = true
"""

pydocstyle_toml = """
ignore = "D203,D212,D413,D416"
"""


def accept_vars():
    BuildVars.build_extra_deps['tests'].extend([
        'pytest>=6',
        'coverage[toml]>=5',
    ])
    BuildVars.build_extra_deps['checks'].extend([
        'tox',
        'doc8>=0.9',
        'flake8',
        'flake8-bugbear',
        'pydocstyle[toml]>=6.1',
        'pygments',
    ])
    BuildVars.build_pyproject_sections['tool.pytest.ini_options'].extend(
        pytest_toml.strip().split('\n')
    )

    fmt = {'source_dir': (
        'src' if SourceVars.source_use_src_dir else SourceVars.source_full_dir
    )}
    BuildVars.build_pyproject_sections['tool.coverage.run'].extend(
        coverage_run_toml.format(**fmt).strip().split('\n')
    )
    BuildVars.build_pyproject_sections['tool.coverage.report'].extend(
        coverage_report_toml.strip().split('\n')
    )
    BuildVars.build_pyproject_sections['tool.pydocstyle'].extend(
        pydocstyle_toml.strip().split('\n')
    )
    BuildVars.build_manifest_in_items = getattr(
        BuildVars, 'build_manifest_in_items', []
    )
    BuildVars.build_manifest_in_items.append('graft tests')
    GitignoreVars.gitignore_items.extend([
        '.tox/',
        '.coverage',
        'coverage.xml',
    ])


tool = Tool(
    module,
    'pytest+tox',
    'Pytest and linters with Tox configuration',
    depends=[source, build],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
