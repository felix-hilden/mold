from mold import Tool, templates_from_directory
from ...domains import python, module
from ...categories import license_ as license_category
from ...face.license import interface as license_, Provides
from ...face.doc import Accepts as DocVars
from ...face.readme import Accepts as ReadmeVars
from ...face.package_readme import Accepts as PackageReadmeVars

badge_lines = """
.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://choosealicense.com/licenses/mit
   :alt: License: MIT\
"""


def provide_vars():
    Provides.license_shorthand = 'MIT'


def accept_vars():
    header = '|license|'
    footer = badge_lines.split('\n')
    DocVars.doc_header_lines.append(header)
    DocVars.doc_footer_lines.extend(footer)
    ReadmeVars.readme_header_lines.append(header)
    ReadmeVars.readme_footer_lines.extend(footer)
    PackageReadmeVars.package_readme_header_lines.append(header)
    PackageReadmeVars.package_readme_footer_lines.extend(footer)


tool = Tool(
    module,
    'MIT',
    'permissive MIT license',
    depends=[license_],
    category=license_category,
    templates=templates_from_directory(__file__),
    provide_vars=provide_vars,
    accept_vars=accept_vars,
)
python.add_tool(tool)
