from typing import List
from mold import Interface, Link
from ..domains import module


class Provides:
    pass


class Accepts:
    package_readme_header_lines: List[str] = []
    package_readme_links: List[Link] = []
    package_readme_footer_lines: List[str] = []


interface = Interface(
    module,
    'package readme',
    'simple readme file for a package manager',
    Provides,
    Accepts,
)
