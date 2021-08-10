"""
A hook for external modules to attach their domains to.

Provides the guaranteed configuration values:

- :attr:`project_name`
- :attr:`project_slug`
"""

from string import ascii_letters, digits
from typing import List
from .things import Domain, Interface, Question

_domains: List[Domain] = []


def add_domain(domain: Domain):
    """Add domain to the pool of alternatives."""
    _domains.append(domain)


class Provides:
    """Global domain provides variables."""

    project_name: str = ''
    project_slug: str = ''


class Accepts:
    """Global domain accepts variables."""


_project_questions = [
    Question('project_name', 'project name'),
    Question('project_slug', 'project slug (leave empty to generate from name)'),
]


def _post_dialog():
    Provides.project_name = _project_questions[0].response
    project_slug = _project_questions[1].response
    if not project_slug:
        accepted = ascii_letters + digits + ' -'
        clean = ''.join([t for t in Provides.project_name if t in accepted])
        project_slug = clean.lower().replace(' ', '-')
    Provides.project_slug = project_slug


_project_interface = Interface(
    'mold_global',
    'project',
    'default configuration for all projects',
    Provides,
    Accepts,
    questions=_project_questions,
    post_dialog=_post_dialog,
)
