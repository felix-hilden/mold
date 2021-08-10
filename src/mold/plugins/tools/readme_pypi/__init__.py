from mold import Tool, Link, templates_from_directory, hook
from ...domains import python, module
from ...face.package_readme import interface as pypi_readme, Accepts
from ...face.doc import Accepts as DocVars
from ...face.build import (
    interface as build, Provides as BuildProvides, Accepts as BuildAccepts
)
from ...face.readme import interface as readme, Accepts as ReadmeVars


pyversions_badge = """
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/{slug}
   :alt: Python versions\
"""

downloads_badge = """
.. |downloads| image:: https://img.shields.io/pypi/dm/{slug}
   :alt: monthly downloads\
"""

pypi_badge = """
.. |pypi| image:: https://img.shields.io/pypi/v/{slug}.svg
   :target: https://pypi.org/project/{slug}
   :alt: PyPI package\
"""


def accept_vars() -> None:
    slug = hook.Provides.project_slug

    Accepts.package_readme_header_lines.append('|pyversions|')
    Accepts.package_readme_footer_lines.extend(
        pyversions_badge.format(slug=slug).split('\n')
    )
    Accepts.package_readme_header_lines.append('|downloads|')
    Accepts.package_readme_footer_lines.extend(
        downloads_badge.format(slug=slug).split('\n')
    )

    BuildAccepts.build_readme_file = 'readme_pypi.rst'
    link = Link(BuildProvides.build_download_url, 'PyPI', 'Package on')
    ReadmeVars.readme_header_lines.append('|pypi|')
    ReadmeVars.readme_links.append(link)
    ReadmeVars.readme_footer_lines.extend(pypi_badge.format(slug=slug).split('\n'))
    DocVars.doc_header_lines.append('|pypi|')
    DocVars.doc_links.append(link)
    DocVars.doc_footer_lines.extend(pypi_badge.format(slug=slug).split('\n'))


tool = Tool(
    module,
    'pypi readme',
    'basic PyPI readme file using RST',
    depends=[pypi_readme, readme, build],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
