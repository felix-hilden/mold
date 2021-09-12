.. _tutorial:

Tutorial
========

Initialising projects
---------------------
Initialising a new project is the default action of Mold.
Optionally you can specify the name of the configuration to be used.
If none is specified, a dialog will determine the configuration.

.. code:: sh

   $ mold
   $ mold python-project

A series of dialogs follows that finalise the configuration
and provide project metadata.
Finally the files are written to a new folder in the current working directory.
See the :ref:`cli` for details and more options.

Creating configurations
-----------------------
The default configurations are meant to serve as a starting point.
It is possible to customise the tools applied to your projects.
See the :ref:`cli` for details and more options.

.. code:: sh

   $ mold config new [config name]

Prefilling values
-----------------
Some project metadata doesn't really change, like email addresses or usernames.
To further reduce hassle when initialising projects,
these values can be prefilled and applied to projects automatically.
See the :ref:`cli` for details and more options.

.. code:: sh

   $ mold prefill

Custom extensions
-----------------
Mold is built for modularity.
Making custom extensions, like implementing new tools and templates,
is straight forward with a builtin source code example.
See :ref:`reference` for more details.
If the tool is something that could be applicable to many users,
please open a feature request on the
`issue tracker <https://github.com/felix-hilden/mold/issues>`_!
