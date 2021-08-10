from typing import List
from mold import Interface, Link
from ..domains import module


class Provides:
    pass


class Accepts:
    doc_header_lines: List[str] = []
    doc_links: List[Link] = []
    doc_footer_lines: List[str] = []


interface = Interface(
    module,
    'documentation',
    'documentation engine of the project',
    Provides,
    Accepts,
)
