from typing import List
from mold import Interface, Question, Link
from ..domains import module


class Provides:
    readme_description: str = ''


class Accepts:
    readme_header_lines: List[str] = []
    readme_example_lines: List[str] = []
    readme_links: List[Link] = []
    readme_footer_lines: List[str] = []


questions = [Question('readme_description', 'project description')]


def post_dialog():
    Provides.readme_description = questions[0].response


interface = Interface(
    module,
    'readme',
    'simple readme file',
    Provides,
    Accepts,
    questions=questions,
    post_dialog=post_dialog,
)
