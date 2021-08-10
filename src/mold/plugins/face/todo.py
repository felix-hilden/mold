from typing import List

from mold import Interface
from ..domains import module


class Provides:
    pass


class Accepts:
    todo_items: List[str] = []


interface = Interface(
    module,
    'todo',
    'TODO file pre-filled by other tools',
    Provides,
    Accepts,
)
