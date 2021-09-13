"""Mold configuration management."""
from textwrap import indent
from .. import hook
from ..config import (
    write_config,
    delete_config,
    read_all_configs,
    read_config,
    concretise_config,
    abstract_config,
    find_by_repr,
    ObjConfig,
    gather_categories,
)
from ..things import Tool


def configure_show(name: str = None):
    """Show information about a config."""
    config = select_config(name)
    config = concretise_config(config, hook._domains)
    print(f'\nCONFIGURATION "{config.name}":')
    print(f'Domain: {config.domain.name} ({config.domain.description})')
    print('Components:')
    for c in config.components:
        t = 'Tool' if isinstance(c, Tool) else 'Category'
        print(f' - {c.name}: {c.description} ({t})')

    files = {
        temp.target_path
        for comp in config.components if isinstance(comp, Tool)
        for temp in comp.templates()
    }
    parts = {}
    for file in files:
        top = parts
        for part in file.parts:
            top[part] = top.get(part, {})
            top = top[part]

    print('\nFiles written by the configuration:')
    print_dir_recur(parts)


def configure_del(name: str = None):
    """Delete a configuration."""
    config = select_config(name)
    delete_config(config.name)


def select_config(name: str = None):
    """Select configuration."""
    if name is None:
        configs = read_all_configs()
        print_configs(configs)
        return select_one(configs)
    else:
        return read_config(name)


def print_dir_recur(parts: dict, in_level: int = 1):
    """Print directory structure."""
    for part in sorted(parts, key=lambda k: k.lower()):
        print('    ' * in_level + part, end='')
        if parts[part]:
            print('/')
            print_dir_recur(parts[part], in_level + 1)
        else:
            print()


def domain_repr(domain):
    """Return repr for a domain."""
    return str(domain)


def tool_or_category_repr(thing, category_tools: dict):
    """Determine appropriate repr for a tool or category."""
    if isinstance(thing, Tool):
        r = str(thing) + ' (Tool)'

        if getattr(thing, 'depends', None):
            names = [dep.name for dep in thing.depends if isinstance(dep, Tool)]
            if names:
                r += '\n  - Requires ' + ', '.join(names)
    else:
        r = str(thing) + ' (Category)'

        reprs = [
            indent(tool_or_category_repr(tool, category_tools), '  ')[2:]
            for tool in category_tools[thing]
        ]
        r += ''.join([f'\n  - Contains {r}' for r in reprs])
    return r


def print_choices(choices: list) -> None:
    """Print component choices."""
    spaces = len(str(len(choices)))
    for i, choice in enumerate(choices):
        indented = indent(choice, ' ' * spaces)
        print(f'{i:{spaces}}:', indented[spaces:])


def configure_new(name: str = None):
    """Create a new configuration."""
    if name is None:
        name = input('\nConfiguration name: ')

    print('\nDomains:')
    print_choices([domain_repr(d) for d in hook._domains])
    domain = select_one(hook._domains)

    category_tools = gather_categories(domain.tools)
    available_categories = [k for k in category_tools.keys() if k is not None]
    top_choices = available_categories + category_tools[None]

    print(f'\nTools and categories for {domain.name}:')
    print_choices([tool_or_category_repr(c, category_tools) for c in top_choices])
    choices = select_many(top_choices)

    print(
        '\nChoose tools from categories, '
        'or leave empty to be selected when initialising.'
    )

    tools = []
    categories = []
    for choice in choices:
        if isinstance(choice, Tool):
            tools.append(choice)
            continue

        print(f'\nTools providing {choice.name}:')
        print_choices([
            tool_or_category_repr(c, category_tools) for c in category_tools[choice]
        ])
        selection = select_one(category_tools[choice], optional=True)
        if selection:
            tools.append(selection)
        else:
            print('  Tool will be chosen on initialisation.')
            categories.append(choice)

    config = ObjConfig(name, domain, tools + categories)
    write_config(abstract_config(config))


def print_configs(configs) -> None:
    """Print available configurations."""
    print('Available configurations:')
    for i, config in enumerate(configs):
        domain = find_by_repr(hook._domains, config.domain)
        print(f'{i}: {config.name}, using domain "{domain.name}"')


def select_many(choices: list) -> list:
    """Choose many from a list."""
    if len(choices) == 1:
        print('Choosing (0) automatically as the only option...')
        return choices

    while True:
        in_ = input('Choose many: ')
        try:
            indices = parse_indices(in_)
            break
        except ValueError:
            print('INVALID INPUT! ', end='')
    return [choices[i] for i in indices]


def select_one(choices: list, optional: bool = False):
    """Choose one from a list."""
    if len(choices) == 1:
        print('Choosing (0) automatically as the only option...')
        return choices[0]

    while True:
        in_ = input(f'Choose one{" (optional)" * optional}: ')

        if optional and not in_:
            print('  Selected none.')
            return

        try:
            return choices[int(in_)]
        except (ValueError, IndexError):
            print('INVALID INPUT! ', end='')


def parse_indices(in_: str) -> list:
    """Parse indices from comma-separated and ranged index string."""
    comps = in_.split(',')
    indices = set()
    for comp in comps:
        if '-' in comp:
            low, high = comp.split('-')
            indices.update(range(int(low), int(high) + 1))
        else:
            indices.add(int(comp))
    return sorted(indices)
