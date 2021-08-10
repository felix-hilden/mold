from mold import Interface, Question, hook
from .doc_host import interface as doc_host, Provides as DocHostVars
from ..domains import module


class Provides:
    rtd_project: str = ''


class Accepts:
    pass


questions = [
    Question('rtd_project', 'RTD project name (leave empty for project slug)'),
]


def post_dialog():
    Provides.rtd_project = questions[0].response or hook.Provides.project_slug
    url = f'https://{Provides.rtd_project}.rtfd.org'
    DocHostVars.doc_host_url = url


interface = Interface(
    module,
    'documentation host',
    'provider for online documentation',
    Provides,
    Accepts,
    parents=[doc_host],
    questions=questions,
    post_dialog=post_dialog,
)
