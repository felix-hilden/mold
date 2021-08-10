from typing import List
from mold import Interface
from ..domains import module


class Provides:
    pass


class Accepts:
    gitignore_items: List[str] = []


interface = Interface(
    module,
    'gitignore',
    'ignore files in git version control',
    Provides,
    Accepts,
)
