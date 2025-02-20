Getting Started
===============

To get started with AppCraft, follow these steps:

Installation
--------------------

To install AppCraft, simply run the following command:

.. code-block:: bash

    pip install appcraft

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

        appcraft init logs locales flask_ui flask_api sqlalchemy

    This will initialize your project with the specified templates. Make sure to separate each template name with a space.
    
- Or, to list available templates
    .. code-block:: bash

        appcraft list_templates

    For more details on available templates, refer to the `Templates Documentation <templates/index.html>`_.