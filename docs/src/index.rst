Mold
====
|license| |pypi|

   "Not the green kind."

Extensible and configurable project initialisation.
We provide a command line tool that generates various types of
text-based projects with simple dialogue.
Mold your new projects to get up to speed quickly and confidently
while following best practices.
Create initialisation configurations to fit your own needs.

.. code:: sh

    $ mold --help
    $ mold python-library

Mold elsewhere:

- Package on `PyPI <https://pypi.org/project/mold>`_
- Development on `GitHub <https://github.com/felix-hilden/mold>`_

Quick start
-----------
First, install Mold from PyPI.

.. code:: sh

    $ pip install mold

Then initialise a Python package with the builtin configuration.

.. code:: sh

    $ mold python-library

A series of dialogs will determine the most important information required to
initialise a working library with all the necessary development tools.
You might also be interested in viewing all builtin configurations
or a specific configuration in more detail.

.. code:: sh

    $ mold config list
    $ mold config show python-library

Mission
-------
We aim to be the fastest and simplest way of creating
text-based projects that have a preset structure.
The trouble from starting a project
to actually begin developing it should be minimised.
The bulk of the work is moved to configuration
that can be applied to new projects repeatedly.

Although Mold is extensible, the builtin system is opinionated
and project initialisations shouldn't be considered configurable
beyond specifying project metadata.
Different structural or tool choices are implemented as plugins
and attached to configurations for repeated initialisation.

While experienced users get value from the speedy setup,
inexperienced users benefit from the preset tools even more.
Less time is used when searching for ways to use the most common tools,
figuring out how they are used, and debugging setup errors.
Seeing new tools might even spark inspiration to learn more.

.. toctree::
   :hidden:
   :caption: Package

   release_notes
   command_line_reference
   plugins

.. toctree::
   :hidden:
   :caption: For developers

   developer_reference
   contributing

.. toctree::
   :hidden:
   :caption: Links

   GitHub ↪ <https://github.com/felix-hilden/mold>
   PyPI ↪ <https://pypi.org/project/mold>

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://choosealicense.com/licenses/mit
   :alt: License: MIT

.. |pypi| image:: https://img.shields.io/pypi/v/mold.svg
   :target: https://pypi.org/project/mold
   :alt: PyPI package
