from typing import Dict, List
from collections import defaultdict

from mold import Interface, Question, hook
from .doc_host import Provides as DocHostVars
from ..domains import module


class Provides:
    build_email: str = ''
    build_keywords: str = ''
    build_url: str = ''
    build_download_url: str = ''


class Accepts:
    build_readme_file: str = ''
    build_extra_deps: Dict[str, List[str]] = defaultdict(list)
    build_project_urls: Dict[str, str] = {}
    build_pyproject_sections: Dict[str, List[str]] = defaultdict(list)
    build_entry_points: Dict[str, List[str]] = defaultdict(list)


questions = [
    Question('build_email', 'package author email'),
    Question('build_keywords', 'package keywords (space separated)')
]


def post_dialog():
    Provides.build_email = questions[0].response
    Provides.build_keywords = questions[1].response

    pypi_url = f'https://pypi.org/project/{hook.Provides.project_slug}'
    Provides.build_url = DocHostVars.doc_host_url or pypi_url
    Provides.build_download_url = pypi_url


interface = Interface(
    module,
    'build',
    'project build provider and dependencies',
    Provides,
    Accepts,
    questions=questions,
    post_dialog=post_dialog,
)
