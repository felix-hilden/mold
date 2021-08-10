"""
Needs doc_host_url from child.
"""
from mold import Interface
from ..domains import module


class Provides:
    doc_host_url: str = ''


class Accepts:
    pass


interface = Interface(
    module,
    'documentation host',
    'provider for online documentation',
    Provides,
    Accepts,
)
