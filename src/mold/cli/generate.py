"""Mold project generation."""
from pathlib import Path
from collections import defaultdict

from jinja2 import TemplateSyntaxError

from .. import Tool, Interface, hook
from ..config import read_config, read_all_configs
from ..template import write, render, undeclared_vars
from .configure import (
    check_dependencies, print_configs, select_one, concretise_config
)


def generate(name: str = None, add: bool = False):
    """Generate project files."""
    if name:
        config = read_config(name)
    else:
        configs = read_all_configs()
        print_configs(configs)
        config = select_one(configs)

    config = concretise_config(config, hook._domains)

    tools_set = set(config.tools)
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

    faces_set = set()
    for tool in tools:
        face_deps = [d for d in tool.depends if isinstance(d, Interface)]
        faces_set.update(gather_interfaces(face_deps))

    faces = []
    while True:
        for face in list(faces_set):
            if all(p in faces for p in face.parents):
                faces.append(face)
                faces_set.discard(face)
        if not faces_set:
            break

    faces.insert(0, hook._project_interface)

    print('\nConfigure project:')
    for face in faces:
        for question in face.questions:
            question.response = input(question.prompt.capitalize() + ': ')

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
    for tool in config.tools:
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


def gather_interfaces(interfaces) -> set:
    """Recursively determine all connected interfaces."""
    faces = set(interfaces)
    for face in interfaces:
        faces.update(gather_interfaces(face.parents))
    return faces
