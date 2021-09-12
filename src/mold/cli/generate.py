"""Mold project generation."""
from pathlib import Path
from collections import defaultdict

from jinja2 import TemplateSyntaxError

from .. import Tool, Interface, hook
from ..template import write, render, undeclared_vars
from ..config import gather_categories, load_prefilled
from .configure import (
    concretise_config, select_config, select_one, print_choices, tool_or_category_repr
)


def generate(name: str = None, add: bool = False):
    """Generate project files."""
    config = select_config(name)
    config = concretise_config(config, hook._domains)

    categories = []
    single_tools = []
    for comp in config.components:
        if isinstance(comp, Tool):
            single_tools.append(comp)
        else:
            categories.append(comp)

    tool_deps = {
        dep for tool in single_tools for dep in tool.depends if isinstance(dep, Tool)
    }
    category_tools = gather_categories(config.domain.tools)
    select_tools = []
    print('\nChoose tools from categories:')
    for category in categories:
        cat_tools = category_tools[category]
        common = set(cat_tools).intersection(tool_deps)
        if len(common) > 1:
            print(f'Cannot fulfill dependencies with category {category}')
            exit(1)
        if len(common) == 1:
            tool = list(common)[0]
            print(f'Selecting {tool} as the only valid option in {category}')
            select_tools.append(tool)
        else:
            print(f'\nTools providing {category.name}:')
            print_choices([tool_or_category_repr(t, category_tools) for t in cat_tools])
            choice = select_one(cat_tools, optional=True)
            if choice:
                select_tools.append(choice)

    tools_set = set(single_tools + select_tools)
    tools = []
    while True:
        for tool in list(tools_set):
            deps = [d for d in tool.depends if isinstance(d, Tool)]
            if all(d in tools for d in deps):
                tools.append(tool)
                tools_set.discard(tool)
        if not tools_set:
            break

    check_dependencies(tools)
    faces = gather_interfaces(tools)
    prefilled = load_prefilled()

    print('\nConfigure project:')
    for face in faces:
        for question in face.questions:
            question.response = prefilled.get(question.id) or dialog(question.prompt)

    for face in faces:
        face.post_dialog()

    for tool in tools:
        tool.provide_vars()

    for tool in tools:
        tool.accept_vars()

    for tool in tools:
        tool.handle_accept()

    variables = {}
    for face in faces:
        variables.update(face.get_namespace_dict(face.provides))
        variables.update(face.get_namespace_dict(face.accepts))

    tool_templates = {}
    for tool in tools:
        tool_templates[tool] = tool.templates()

    template_vars = defaultdict(set)
    target_paths = set()

    for templates in tool_templates.values():
        for template in templates:
            path = str(template.target_path)
            try:
                undeclared = undeclared_vars(template.content) | undeclared_vars(path)
            except TemplateSyntaxError as e:
                print('Template content:')
                print(template.content)
                print('Template path:', path)
                raise ValueError('Incorrect template syntax: ' + str(e)) from e
            template_vars[path].update(undeclared)

            if template.target_path in target_paths:
                raise FileExistsError('Template already defined')

            target_paths.add(template.target_path)

    variables.update(Interface.get_namespace_dict(hook.Provides))

    missing = {}
    for path, t_vars in template_vars.items():
        undeclared = t_vars - set(variables.keys())
        if undeclared:
            missing[path] = undeclared

    if missing:
        msg = '\n'.join([
            f'    {path}: {", ".join(undeclared)}'
            for path, undeclared in missing.items()
        ])
        raise ValueError('Undeclared variables found in templates:\n' + msg)

    top_dir = Path('./{{ project_slug }}')
    for tool, templates in tool_templates.items():
        ready = []
        for template in templates:
            text = render(template.content, variables)
            file = Path(render(str(top_dir / template.target_path), variables))
            ready.append((file, text))

        if add:
            exist = [file for file, _ in ready if file.exists()]
            if exist:
                print(f'Skipping {tool} - some files exist already:')
                for file in exist:
                    print('  - ' + str(file))
                continue
            print(f'Writing {tool}...')

        for file, text in ready:
            write(file, text)


def gather_interfaces(tools: list) -> list:
    """Gather all interfaces of tools."""
    faces_set = set()
    for tool in tools:
        face_deps = [d for d in tool.depends if isinstance(d, Interface)]
        faces_set.update(tool_interfaces(face_deps))

    faces = []
    while True:
        for face in list(faces_set):
            if all(p in faces for p in face.parents):
                faces.append(face)
                faces_set.discard(face)
        if not faces_set:
            break

    faces.insert(0, hook._project_interface)
    return faces


def tool_interfaces(interfaces) -> set:
    """Recursively determine all connected interfaces."""
    faces = set(interfaces)
    for face in interfaces:
        faces.update(tool_interfaces(face.parents))
    return faces


def dialog(prompt) -> str:
    """Format prompt and perform dialog."""
    return input(prompt.capitalize() + ': ')


def check_dependencies(tools) -> None:
    """Check that a set of tools fulfills its dependencies."""
    for tool in tools:
        deps = [d for d in tool.depends if isinstance(d, Tool)]
        assert all([t in tools for t in deps])

    category_tools = gather_categories(tools)
    categories = [c for c in category_tools.keys() if c is not None]
    for c in categories:
        if len(category_tools[c]) > 1:
            raise ValueError('More than one tool for a category!')
