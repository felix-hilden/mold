"""Jinja template operations."""
from pathlib import Path

from jinja2 import Environment, Template
from jinja2.meta import find_undeclared_variables


def undeclared_vars(content: str):
    """Find undeclared Jinja variables in content."""
    return find_undeclared_variables(Environment().parse(content))


def render(content, variables) -> str:
    """Render content with assigned variables."""
    return Template(content, keep_trailing_newline=True).render(**variables)


def write(file: Path, text: str):
    """Write text to a non-empty file."""
    if file.exists():
        raise FileExistsError('Template would overwrite existing file: ' + str(file))
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding='utf-8')
