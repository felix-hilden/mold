"""Mold configuration management."""
from collections import defaultdict
from textwrap import indent
from typing import List, Dict, Optional
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
)
from ..things import Tool, Category


def configure_show(name: str = None):
    """Show information about a config."""
    if name is None:
        configs = read_all_configs()
        print_configs(configs)
        config = select_one(configs)
    else:
        config = read_config(name)

    config = concretise_config(config, hook._domains)
    print(f'\nCONFIGURATION "{config.name}":')
    print(f'Domain: {config.domain.name} ({config.domain.description})')
    print('Tools:')
    for t in config.tools:
        msg = f' - {t.name}: {t.description}'
        if t.category:
            msg += f' (providing {t.category.name}: {t.category.description})'
        print(msg)


def configure_del(name: str = None):
    """Delete a configuration."""
    if name is None:
        configs = read_all_configs()
        print_configs(configs)
        name = select_one(configs).name
    delete_config(name)


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

    while True:
        print(f'\nTools and categories for {domain.name}:')
        print_choices([tool_or_category_repr(c, category_tools) for c in top_choices])
        choices = select_many(top_choices)

        tools = []
        for choice in choices:
            if isinstance(choice, Tool):
                tools.append(choice)
                continue

            print(f'\nTools providing {choice.name}:')
            print_choices([
                tool_or_category_repr(c, category_tools) for c in category_tools[choice]
            ])
            tools.append(select_one(category_tools[choice]))

        try:
            check_dependencies(tools)
            break
        except AssertionError:
            print('Invalid configuration, dependencies not satisfied!')

    config = ObjConfig(name, domain, tools)
    write_config(abstract_config(config))


def gather_categories(tools: List[Tool]) -> Dict[Optional[Category], List[Tool]]:
    """Transpose a list of tools to be indexed with their associated categories."""
    category_tools = defaultdict(list)
    for tool in tools:
        category_tools[tool.category].append(tool)
    return category_tools


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


def select_one(choices: list):
    """Choose one from a list."""
    if len(choices) == 1:
        print('Choosing (0) automatically as the only option...')
        return choices[0]

    while True:
        in_ = input('Choose one: ')
        try:
            return choices[int(in_)]
        except (ValueError, IndexError):
            print('INVALID INPUT! ', end='')


def check_dependencies(tools):
    """Check that a set of tools fulfills its dependencies."""
    for tool in tools:
        deps = [d for d in tool.depends if isinstance(d, Tool)]
        assert all([t in tools for t in deps])

    category_tools = gather_categories(tools)
    categories = [c for c in category_tools.keys() if c is not None]
    for c in categories:
        if len(category_tools[c]) > 1:
            raise ValueError('More than one tool for a category!')


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
