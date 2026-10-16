Getting Started
===============

What Is Appcraft?
-----------------

Appcraft is a code generator for Python projects: ``appcraft init`` scaffolds a new project already organized into Clean Architecture layers (domain, application, infrastructure, presentation, runners — see :doc:`architecture/index`), and from there you keep developing inside it like any other Python project. It is not a library your code imports at runtime, beyond a handful of small utilities the generated project ships with itself.

Why Use It
----------

- **A consistent structure from the first commit.** Business rules (domain/application) stay separate from frameworks and storage (infrastructure), so a project doesn't accumulate ad hoc structure as it grows, and the same conventions apply whether you built it alone or picked it up from someone else.
- **Add only what the project needs.** Functionality comes from composable **templates** — ``flask_api``, ``sqlalchemy``, ``docker``, ``git``, and more (see :doc:`templates/index`). Installing one drops its files and wires itself in automatically: a new Flask route or a new SQLAlchemy model is picked up without touching a central registration file.
- **Swap infrastructure without rewriting business logic.** Interchangeable templates sit behind the same contract (a ``Port``) — ``sqlalchemy``/``mongodb`` for the database, ``selenium``/``playwright``/``httpx``/``curl_cffi`` for web scraping. Changing which one is installed, or which one a config file prefers, doesn't change the use case that calls it.
- **One command style for every feature.** Every command, from the application's own entry points to one-off maintenance tasks, runs through the same **runner** system: an interactive menu for a human, and ``interactive=false`` with ``key=value`` arguments for a script or CI — see :doc:`developing/index`.
- **You own what gets generated.** Every file Appcraft drops is plain, readable Python in your project. Templates only keep checking each other's presence at runtime (``is_installed()``) so they can adapt to what's installed — Appcraft itself doesn't need to run again once the project exists, except when you choose to add another template.

Use it when starting a new service or tool that's worth keeping organized as it grows. For a quick throwaway script, the scaffolding is more than you need.

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

    ``appc`` is a shorter alias for ``appcraft``: ``appc init flask_ui`` does the same thing. Inside a project, ``appc run <module> <method>`` and ``appc tools <module> <method>`` run the project's own ``run`` and ``tools`` launchers, the same as ``python run`` and ``python tools``.
    
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