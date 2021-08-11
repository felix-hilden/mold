"""Utilities for creating plugin documentation."""
from pathlib import Path
from importlib import import_module
from functools import lru_cache
from typing import List

from ..template import render as render_template
from ..things import Category, Domain, Interface, Tool


@lru_cache(maxsize=None)
def _get_template(type_: str):
    valid = ('category', 'domain', 'interface', 'tool')
    if type_ not in valid:
        raise ValueError(f'Invalid template type! Expected one of {valid}')

    file = Path(__file__).parent / f'{type_}.rst.temp'
    return file.read_text('utf-8')


def render_doc(import_location: str) -> str:
    """
    Render documentation for any Mold component.

    The component is imported and introspected to determine the appropriate
    documentation template, which is filled with the component's attributes.

    Parameters
    ----------
    import_location
        dotted name leading to the component, e.g. ``mold.plugins.domains.python``
    """
    *from_parts, name = import_location.split('.')
    from_ = '.'.join(from_parts)

    try:
        thing = getattr(import_module(from_), name, None)
    except ModuleNotFoundError:
        thing = None

    if isinstance(thing, Category):
        type_ = 'category'
    elif isinstance(thing, Domain):
        type_ = 'domain'
    elif isinstance(thing, Interface):
        type_ = 'interface'
    elif isinstance(thing, Tool):
        type_ = 'tool'
    else:
        msg = f'Invalid import location: {import_location} with type {type(thing)}!'
        raise ValueError(msg)

    return render_template(
        _get_template(type_), dict(s=thing, import_location=import_location)
    )


_plugins_template = """
.. _plugins:

Available plugins
=================
{intro_text}

"""


def _type_docs(category: str, locations: List[str]) -> str:
    head = category.capitalize() + '\n' + '-' * len(category) + '\n'
    texts = [render_doc(loc) for loc in locations]
    return head + '\n'.join(texts) + '\n'


def render_docs(
    intro_text: str,
    domain_locations: List[str] = None,
    tool_locations: List[str] = None,
    category_locations: List[str] = None,
    interface_locations: List[str] = None,
) -> str:
    """
    Render documentation for Mold components.

    Components are documented with :func:`render_doc`
    and gathered by type to a single document
    whose main heading has a reference ``plugins``.

    Parameters
    ----------
    intro_text
        text to include under the main header
    domain_locations
        domain import locations
    tool_locations
        tool import locations
    category_locations
        category import locations
    interface_locations
        interface import locations
    """
    text = _plugins_template.format(intro_text=intro_text)

    if domain_locations:
        text += _type_docs('domains', domain_locations)
    if tool_locations:
        text += _type_docs('tools', tool_locations)
    if category_locations:
        text += _type_docs('categories', category_locations)
    if interface_locations:
        text += _type_docs('interfaces', interface_locations)

    return text
