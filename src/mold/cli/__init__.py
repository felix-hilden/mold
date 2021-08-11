"""Mold CLI implementation."""
import pkg_resources
import sys

from ..config import read_all_configs
from .generate import generate
from .configure import configure_new, configure_show, configure_del, print_configs


mold_help = """Extensible and configurable project initialisation.

usage: mold [configuration] [--help] [--version]
       mold add [configuration]
       mold config <command> [arg]

COMMANDS:
[configuration]     Initialise a new project.
add [configuration] Add files to an existing project. All files
                    that a tool would write must be missing for
                    them to be added to the project.

config list         List all saved configurations.
config new [name]   Create a new configuration.
config show [name]  Show a configuration.
config del [name]   Delete a configuration.

--help, -h          Display this help message and quit.
--version, -v       Display Mold version and quit.

Missing optional parameters are determined with a dialog."""


def main():
    """Execute main CLI entry point."""
    mode = _maybe_argument(1)
    if mode in ('-h', '--help'):
        print(mold_help)
        return
    elif mode in ('-v', '--version'):
        from .. import __version__
        print(f'mold v{__version__}')
        return

    load_entry_points()
    if mode == 'config':
        configure(_maybe_argument(2), _maybe_argument(3))
    elif mode == 'add':
        generate(_maybe_argument(2), add=True)
    else:
        generate(mode)


def configure(command: str = None, name: str = None):
    """Configure menu."""
    if command == 'new':
        configure_new(name)
    elif command == 'show':
        configure_show(name)
    elif command == 'del':
        configure_del(name)
    elif command == 'list':
        print_configs(read_all_configs())
    else:
        print('Missing sub command! See help below.\n')
        print(mold_help)
        exit(1)


def load_entry_points():
    """Load available plugins from entry points."""
    for entry_point in pkg_resources.iter_entry_points('mold.plugins'):
        entry_point.load()


def _maybe_argument(index: int):
    return sys.argv[index] if len(sys.argv) > index else None
