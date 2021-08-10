"""Mold constructs."""
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union, Callable


@dataclass
class Question:
    """Question dialog."""

    id: str
    prompt: str
    response: str = field(init=False, default_factory=str)


@dataclass
class Template:
    """Jinja2 template file."""

    target_path: Path
    content: str


@dataclass
class Link:
    """Tool-agnostic way of representing hyperlinks."""

    target: str
    text: str
    pre_text: str = None


@dataclass(repr=False, eq=False)
class Component(ABC):
    """Mold component base."""

    module: str
    name: str
    description: str

    def __repr__(self):
        """Return component information."""
        return self.module + '-' + self.name

    def __str__(self):
        """Return readable information about a component."""
        return f'{self.name} - {self.description} (from {self.module})'


Procedure = Callable[[], None]


@dataclass(repr=False, eq=False)
class Interface(Component):
    """
    Tool interface that provides and accepts configuration, and provides dialog.

    Parameters
    ----------
    post_dialog
        this interface must provide the variables in "Provides"
        and may use the provided variables of dependencies
    """

    provides: type
    accepts: type
    parents: List['Interface'] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)
    post_dialog: Procedure = field(default_factory=lambda: lambda: None)

    @staticmethod
    def get_namespace_dict(namespace) -> dict:
        """Parse variables from a namespace, i.e. provides and accepts."""
        return {
            var: getattr(namespace, var)
            for var in dir(namespace)
            if not var[0] == '_'
        }


def templates_from_directory(init_file: str) -> Callable[[], List[Template]]:
    """Generate templates from a directory "templates" relative to path."""
    def wrapper() -> List[Template]:
        folder = Path(init_file).parent / 'templates'
        return [
            Template(p.relative_to(folder).with_suffix(''), p.read_text('utf-8'))
            for p in folder.glob('**/*.temp')
        ]
    return wrapper


@dataclass(repr=False, eq=False)
class Category(Component):
    """Collection of tools that should be mutually exclusive."""


@dataclass(repr=False, eq=False)
class Tool(Component):
    """
    Tool implementation.

    Parameters
    ----------
    provide_vars
        this loader must provide the variables in "Provides",
        it may also modify the variables in "Accepts" or the accepted variables
        of other loaders
    accept_vars
        this loader and other loaders may modify the accepted variables,
        this loader may modify the provided variables using the provided variables
        of other loaders that are depended on
    handle_accept
        this loader may modify the accepted variables
    """

    depends: List[Union['Tool', Interface]]
    category: Category = None
    templates: Callable[[], List[Template]] = field(default_factory=lambda: lambda: [])
    provide_vars: Procedure = field(default_factory=lambda: lambda: None)
    accept_vars: Procedure = field(default_factory=lambda: lambda: None)
    handle_accept: Procedure = field(default_factory=lambda: lambda: None)


@dataclass(repr=False, eq=False)
class Domain(Component):
    """
    Project domain.

    Connects all relevant tools together.
    """

    tools: List[Tool] = field(init=False, default_factory=list)

    def add_tool(self, tool: Tool):
        """Register a tool to this domain."""
        self.tools.append(tool)
