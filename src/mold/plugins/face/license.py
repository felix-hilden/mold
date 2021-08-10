"""
Needs license_shorthand from tools.
"""
from mold import Interface, Question
from ..domains import module


class Provides:
    license_author: str = ''
    license_years: str = ''
    license_shorthand: str = ''


class Accepts:
    pass


questions = [
    Question('license_author', 'package author'),
    Question('license_first_year', 'first year of license (leave blank for current)'),
]


def post_dialog():
    Provides.license_author = questions[0].response
    Provides.license_years = questions[1].response or '2021'


interface = Interface(
    module,
    'license',
    'license applied to the project',
    Provides,
    Accepts,
    questions=questions,
    post_dialog=post_dialog,
)
