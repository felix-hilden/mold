from mold import Tool, templates_from_directory
from ...domains import python, module
from ...categories import gitignore as gitignore_category
from ...face.gitignore import interface as gitignore, Accepts

sections = {
    'Python files': [
        '__pycache__/',
        '*.py[cod]',
        '*$py.class',
        '*.so',
        '__pypackages__/',
    ],
    'Distribution / packaging': [
        '.Python',
        '/build/',
        '/develop-eggs/',
        '/dist/',
        '/downloads/',
        '/eggs/',
        '/.eggs/',
        '/lib/',
        '/lib64/',
        '/parts/',
        '/sdist/',
        '/var/',
        '/wheels/',
        '/share/python-wheels/',
        '/.installed.cfg',
        '*.egg-info/',
        '*.egg',
        '/MANIFEST',
    ],
    'Testing': [
        'htmlcov/',
        '.tox/',
        '.nox/',
        '.coverage',
        '.coverage.*',
        '.cache',
        'nosetests.xml',
        'coverage.xml',
        '*.cover',
        '*.py,cover',
        '.hypothesis/',
        '.pytest_cache/',
        'cover/',
    ],
    'Documentation': [
        '/docs/_build/',
        '/docs/build/',
        '/site/',
    ],
    'Notebooks': [
        '.ipynb_checkpoints',
        'profile_default/',
        'ipython_config.py',
    ],
    'Environments': [
        '/.env/',
        '/.venv/',
        '/env/',
        '/venv/',
        '/ENV/',
        '/env.bak/',
        '/venv.bak/',
    ],
    'Type checkers': [
        '.mypy_cache/',
        '.dmypy.json',
        'dmypy.json',
        '.pyre/',
        '.pytype/',
    ],
    'Editors': [
        '.idea/',
        '.vim/',
    ]
}


def handle_accept():
    Accepts.gitignore_sections = sections
    items = set().union(*[set(i) for i in sections.values()])
    unique = set(Accepts.gitignore_items) - items
    Accepts.gitignore_items = list(unique)


tool = Tool(
    module,
    'gitignore for Python',
    'comprehensive gitignore file for Python',
    depends=[gitignore],
    category=gitignore_category,
    templates=templates_from_directory(__file__),
    handle_accept=handle_accept,
)
python.add_tool(tool)
