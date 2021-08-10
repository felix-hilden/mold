from mold import Interface, Question, hook
from .vcs_host import interface as vcs_host, Provides as VcsHostNeeds
from ..domains import module


class Provides:
    github_user: str = ''
    github_repo: str = ''


class Accepts:
    pass


questions = [
    Question('github_user', 'GitHub user name'),
    Question('github_repo', 'GitHub repository (leave empty for project slug)'),
]


def post_dialog():
    user = questions[0].response
    repo = questions[1].response or hook.Provides.project_slug
    Provides.github_user = user
    Provides.github_repo = repo
    VcsHostNeeds.vcs_host_url = f'https://github.com/{user}/{repo}'


interface = Interface(
    module,
    'github',
    'GitHub VCS host',
    Provides,
    Accepts,
    parents=[vcs_host],
    questions=questions,
    post_dialog=post_dialog,
)
