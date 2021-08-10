from mold import Tool, Link, templates_from_directory
from ...domains import python, module
from ...face.doc_host import Provides as DocHostVars
from ...face.read_the_docs import interface as rtd, Provides as RTDVars

from ...face.readme import Accepts as ReadmeVars
from ...face.build import Accepts as BuildVars
from ...face.todo import Accepts as TodoVars
from ...face.source import Accepts as SourceVars
from ...face.package_readme import Accepts as PackageReadmeVars

from ..readme_rst import tool as readme_rst
from ..setuptools import tool as setuptools
from ..sphinx import tool as sphinx

badge_lines = """
.. |readthedocs| image:: {image}
   :target: {target}
   :alt: documentation\
"""


def accept_vars():
    link = Link(DocHostVars.doc_host_url, 'Read The Docs', 'Online documentation on')
    badge_url = f'https://rtfd.org/projects/{RTDVars.rtd_project}/badge/'
    im_latest = badge_url + '?version=latest'
    im_stable = badge_url + '?version=stable'
    target_latest = DocHostVars.doc_host_url + '/en/latest/'
    target_stable = DocHostVars.doc_host_url + '/en/stable/'

    ReadmeVars.readme_header_lines.append('|readthedocs|')
    ReadmeVars.readme_links.append(link)
    ReadmeVars.readme_footer_lines.extend(
        badge_lines.format(image=im_latest, target=target_latest).split('\n')
    )
    PackageReadmeVars.package_readme_header_lines.append('|readthedocs|')
    PackageReadmeVars.package_readme_links.append(link)
    PackageReadmeVars.package_readme_footer_lines.extend(
        badge_lines.format(image=im_stable, target=target_stable).split('\n')
    )

    link_text = f'{link.pre_text} `{link.text} <{link.target}>`_'
    SourceVars.source_doc_lines.append(link_text)
    BuildVars.build_project_urls['Documentation'] = DocHostVars.doc_host_url
    TodoVars.todo_items.append('consider pinning documentation dependencies for RTD')


tool = Tool(
    module,
    'rtd',
    'Read The Docs for Sphinx with badges',
    depends=[rtd, sphinx, readme_rst, setuptools],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
