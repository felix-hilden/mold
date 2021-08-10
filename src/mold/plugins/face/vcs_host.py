"""
Needs vcs_host_url from child interfaces.
"""
from mold import Interface
from ..domains import module


class Provides:
    vcs_host_url: str = ''


class Accepts:
    pass


interface = Interface(
    module,
    'vcs host',
    'online host of the version control system',
    Provides,
    Accepts,
)
