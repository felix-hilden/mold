import setuptools
import os
from pathlib import Path

root = Path(os.path.realpath(__file__)).parent
version_file = root / 'src' / 'mold' / 'VERSION'
readme_file = root / 'readme_pypi.rst'

pypi_url = 'https://pypi.org/project/mold'
github_url = 'https://github.com/felix-hilden/mold'
documentation_url = 'https://pymold.rtfd.org'

extras_require = {
    'build': [
        'build',
        'twine',
    ],
    'docs': [
        'sphinx>=4',
        'sphinx-rtd-theme',
    ],
    'tests': [
        'coverage[toml]>=5',
        'pytest>=6',
    ],
    'checks': [
        'tox',
        'doc8>=0.9',
        'flake8',
        'flake8-bugbear',
        'pydocstyle[toml]>=6.1',
        'pygments',
    ]
}
extras_require['dev'] = sum(extras_require.values(), [])

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
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        'console_scripts': ['mold = mold.cli:main'],
        'mold.plugins': [
            'mold_builtin_plugins = mold.plugins',
        ],
    },

    python_requires='>=3.7',
    install_requires=[
        'Jinja2',
    ],
    extras_require=extras_require,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Testing',
    ],
)
