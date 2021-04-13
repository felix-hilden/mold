import setuptools
import os
from pathlib import Path

root = Path(os.path.realpath(__file__)).parent
version_file = root / 'mold' / 'VERSION'
readme_file = root / 'readme.rst'

pypi_url = 'https://pypi.org/project/mold'
github_url = 'https://github.com/felix-hilden/mold'
documentation_url = 'https://pymold.rtfd.org'

extras_require = {
    'docs': [
        'sphinx',
        'sphinx-rtd-theme',
    ],
    'tests': [
        'coverage',
        'pytest',
    ],
    'checks': [
        'tox',
        'doc8',
        'flake8',
        'flake8-bugbear',
        'pydocstyle',
        'pygments',
    ]
}
extras_require['dev'] = (
    extras_require['docs'] + extras_require['tests'] + extras_require['checks']
)

setuptools.setup(
    name='mold',
    version=version_file.read_text().strip(),
    description='Package / repository initialisation',
    long_description=readme_file.read_text(),
    long_description_content_type='text/x-rst',

    url=documentation_url,
    download_url=pypi_url,
    project_urls={
        'Source': github_url,
        'Issues': github_url + '/issues',
        'Documentation': documentation_url,
    },

    author='Felix Hildén',
    author_email='felix.hilden@gmail.com',
    maintainer='Felix Hildén',
    maintainer_email='felix.hilden@gmail.com',

    license='MIT',
    keywords='package repository template initialisation',
    packages=setuptools.find_packages(exclude=('tests', 'tests.*',)),
    include_package_data=True,
    package_data={
        'mold': ['VERSION']
    },

    python_requires='>=3.6',
    install_requires=[],
    extras_require=extras_require,

    classifiers=[],
)
