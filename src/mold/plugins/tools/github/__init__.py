import subprocess

from mold import Tool, Link, templates_from_directory, hook
from ...domains import python, module
from ...face.vcs_host import Provides
from ...face.package_readme import Accepts as PackageReadmeVars
from ...face.github import interface as github
from ...face.build import Accepts as BuildVars
from ...face.todo import Accepts as TodoVars
from ...face.doc import Accepts as DocVars

_clone_msg = """Clone GitHub repository now?
(Make the repository if you haven't already) Y/[N]: """


def accept_vars():
    url = Provides.vcs_host_url
    BuildVars.build_project_urls['Source'] = url
    BuildVars.build_project_urls['Issues'] = url + '/issues'

    link = Link(url, 'GitHub', 'Development on')
    DocVars.doc_links.append(link)
    PackageReadmeVars.package_readme_links.append(link)

    clone_resp = input(_clone_msg)
    if clone_resp.lower() == 'y':
        subprocess.run(['git', 'clone', f'{url}.git', hook.Provides.project_slug])
    else:
        TodoVars.todo_items.append(
            'set up repository:'
            ' ``git init``,'
            f' ``git remote add origin {url}``,'
            ' ``git fetch``,'
            ' ``git reset origin/<main branch>``'
        )


tool = Tool(
    module,
    'github+templates',
    'GitHub VCS host with issue templates',
    depends=[github],
    templates=templates_from_directory(__file__),
    accept_vars=accept_vars,
)
python.add_tool(tool)
