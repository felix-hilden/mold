"""Mold configuration files."""
import json
from dataclasses import dataclass, asdict
from typing import List
from pathlib import Path
from .things import Domain, Tool

user_configs = Path().home() / '.mold'
builtin_configs = Path(__file__).parent / 'configs'


@dataclass
class StrConfig:
    """Configuration referencing components with strings."""

    name: str
    domain: str
    tools: List[str]


@dataclass
class ObjConfig:
    """Configuration containing dereferenced components."""

    name: str
    domain: Domain
    tools: List[Tool]


def read_config(name: str) -> StrConfig:
    """Read configuration from a file."""
    filename = name + '.json'
    file = user_configs / filename
    if not file.exists():
        file = builtin_configs / filename
    config = json.loads(file.read_text())
    return StrConfig(name, **config)


def write_config(config: StrConfig) -> None:
    """Write configuration to a file."""
    conf_dict = asdict(config)
    name = conf_dict.pop('name')

    name = name + '.json'
    if (builtin_configs / name).exists():
        raise FileExistsError('Cannot overwrite builtin configuration!')

    user_configs.mkdir(parents=True, exist_ok=True)
    file = user_configs / name
    file.write_text(json.dumps(conf_dict, indent=4, sort_keys=True))


def delete_config(name: str) -> None:
    """Delete configuration file."""
    file = user_configs / (name + '.json')
    file.unlink()


def read_all_configs() -> List[StrConfig]:
    """Read all configurations."""
    configs = list(user_configs.glob('*.json')) + list(builtin_configs.glob('*.json'))
    return [read_config(path.stem) for path in configs]


def concretise_config(
    config: StrConfig, available_domains: List[Domain]
) -> ObjConfig:
    """Dereference configuration."""
    domain = find_by_repr(available_domains, config.domain)
    loaders = [find_by_repr(domain.tools, c) for c in config.tools]
    return ObjConfig(config.name, domain, loaders)


def abstract_config(config: ObjConfig) -> StrConfig:
    """Prepare configuration for serialisation."""
    return StrConfig(
        config.name,
        repr(config.domain),
        [repr(d) for d in config.tools],
    )


def find_by_repr(haystack: list, needle: str):
    """Find needle in a haystack."""
    for thing in haystack:
        if repr(thing) == needle:
            return thing
    raise IndexError(f'Not found: {needle}!')
