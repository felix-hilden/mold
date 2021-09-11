from mold import Tool, templates_from_directory
from ...domains import python, module
from ...categories import license_ as license_category
from ...face.license import interface as license_, Provides
from ...face.doc import Accepts as DocVars
from ...face.readme import Accepts as ReadmeVars
from ...face.package_readme import Accepts as PackageReadmeVars

badge_lines = """
.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://choosealicense.com/licenses/bsd-3-clause/
   :alt: License: BSD 3-Clause\
"""


def provide_vars():
    Provides.license_shorthand = 'BSD 3-Clause'


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
    'BSD 3-Clause',
    'permissive license prohibiting use of contributor names in derived products',
    depends=[license_],
    category=license_category,
    templates=templates_from_directory(__file__),
    provide_vars=provide_vars,
    accept_vars=accept_vars,
)
python.add_tool(tool)
