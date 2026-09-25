Getting Started
===============

To get started with AppCraft, follow these steps:

Installation
--------------------

This version of the documentation (|release|) is a pre-release. ``pip`` never installs a pre-release by default, so grab it explicitly with ``--pre``:

.. code-block:: bash

    pip install --pre appcraft

Plain ``pip install appcraft`` (no ``--pre``) installs the latest stable release instead, which won't include what's described on this version of the docs — switch to that release's own documentation via the `version selection page <versions/index.html>`_ if that's what you're running.

Starting a New Project
------------------------------

To start a new project, follow these steps:

1. Create a new directory for your project:
    .. code-block:: bash

        mkdir project_name
        cd project_name

2. Initialize the project using one of the following commands:

- To initialize the project with the desired templates using the following command:
    .. code-block:: bash

        appcraft init <template_names>

- Where `<template_names>` should be replaced by the names of the templates you want to use, separated by spaces. For example:
    .. code-block:: bash

        appcraft init flask_ui flask_api sqlalchemy docker

    This will initialize your project with the specified templates. Make sure to separate each template name with a space.
    
- Or, to list available templates
    .. code-block:: bash

        appcraft list_templates

    For more details on available templates, refer to the `Templates Documentation <templates/index.html>`_.

Adding Templates to an Existing Project
-------------------------------------------

Already have a project and want to add more templates to it? Run ``add_template`` from inside the project directory instead of ``init`` — ``init`` is only for starting a brand new project (and would overwrite what's already there):

.. code-block:: bash

    appcraft add_template <template_names>

For example, adding SQLAlchemy to a project that doesn't have a database template yet:

.. code-block:: bash

    appcraft add_template sqlalchemy

Requesting a template that's exclusive with one you already have (e.g. a different package manager) swaps it in automatically, converting your existing configuration along the way — see `Template Types <templates/concepts/index.html#exclusive-templates>`_.