from mold import Tool, templates_from_directory
from ...domains import python, module
from ...face.readme import Accepts as ReadmeVars
from ...face.vcs_host import Provides as VCSHostVars
from ..github import tool as github
from ..pytest_tox import tool as tests

build_badge = """
.. |build| image:: {vcs_host_url}/workflows/CI/badge.svg
   :target: {vcs_host_url}/actions
   :alt: build status\
"""


def accept_vars():
    fmt = {'vcs_host_url': VCSHostVars.vcs_host_url}
    badge_lines = build_badge.format(**fmt).split('\n')
    ReadmeVars.readme_footer_lines.extend(badge_lines)
    ReadmeVars.readme_header_lines.append('|build|')


tool = Tool(
    module,
    'github actions',
    'GitHub actions with Pytest and Tox',
    depends=[github, tests],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
