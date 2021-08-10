from typing import List
from mold import Interface, hook
from ..domains import module


class Provides:
    source_use_src_dir: bool = True
    source_package_name: str = ''
    source_full_dir: str = ''


class Accepts:
    source_doc_lines: List[str] = []
    source_import_lines: List[str] = []
    source_code_lines: List[str] = []


def post_dialog():
    Provides.source_package_name = hook.Provides.project_slug
    Provides.source_use_src_dir = True
    Provides.source_full_dir = 'src/' + Provides.source_package_name


interface = Interface(
    module,
    'source',
    'project source files',
    Provides,
    Accepts,
    post_dialog=post_dialog,
)
