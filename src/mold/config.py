"""Mold configuration and prefill files."""
import json

from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Union, Dict, Optional
from pathlib import Path
from .things import Domain, Tool, Category

user_configs = Path().home() / '.mold'
builtin_configs = Path(__file__).parent / 'configs'
config_suffix = '.config.json'
prefill_file = user_configs / 'prefill.json'


@dataclass
class StrConfig:
    """Configuration referencing components with strings."""

    name: str
    domain: str
    components: List[str]


@dataclass
class ObjConfig:
    """Configuration containing dereferenced components."""

    name: str
    domain: Domain
    components: List[Union[Tool, Category]]


def read_config(name: str) -> StrConfig:
    """Read configuration from a file."""
    filename = name + config_suffix
    file = user_configs / filename
    if not file.exists():
        file = builtin_configs / filename
    config = json.loads(file.read_text())
    return StrConfig(name, **config)


def write_config(config: StrConfig) -> None:
    """Write configuration to a file."""
    conf_dict = asdict(config)
    name = conf_dict.pop('name')

    name = name + config_suffix
    if (builtin_configs / name).exists():
        raise FileExistsError('Cannot overwrite builtin configuration!')

    user_configs.mkdir(parents=True, exist_ok=True)
    file = user_configs / name
    file.write_text(json.dumps(conf_dict, indent=4, sort_keys=True))


def delete_config(name: str) -> None:
    """Delete configuration file."""
    file = user_configs / (name + config_suffix)
    file.unlink()


def read_all_configs() -> List[StrConfig]:
    """Read all configurations."""
    pattern = '*' + config_suffix
    configs = list(user_configs.glob(pattern)) + list(builtin_configs.glob(pattern))
    return [read_config(path.name.replace(config_suffix, '')) for path in configs]


def concretise_config(
    config: StrConfig, available_domains: List[Domain]
) -> ObjConfig:
    """Dereference configuration."""
    domain = find_by_repr(available_domains, config.domain)
    categories = list(gather_categories(domain.tools).keys())
    loaders = [find_by_repr(domain.tools + categories, c) for c in config.components]
    return ObjConfig(config.name, domain, loaders)


def abstract_config(config: ObjConfig) -> StrConfig:
    """Prepare configuration for serialisation."""
    return StrConfig(
        config.name,
        repr(config.domain),
        [repr(d) for d in config.components],
    )


def find_by_repr(haystack: list, needle: str):
    """Find needle in a haystack."""
    for thing in haystack:
        if repr(thing) == needle:
            return thing
    raise IndexError(f'Not found: {needle}!')


def gather_categories(tools: List[Tool]) -> Dict[Optional[Category], List[Tool]]:
    """Transpose a list of tools to be indexed with their associated categories."""
    category_tools = defaultdict(list)
    for tool in tools:
        category_tools[tool.category].append(tool)
    return category_tools


def load_prefilled():
    """Load prefilled values."""
    if not prefill_file.exists():
        return {}

    return json.loads(prefill_file.read_text())
