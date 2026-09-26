Poetry Template
=============================

The **Poetry Template** manages your project's dependencies with **Poetry**. It's the default — every project starts on it automatically, whether or not you name it explicitly.

It's an `exclusive template <../concepts/index.html#exclusive-templates>`_: it can't be installed alongside `Pipenv <../pipenv/index.html>`_ or `uv <../uv/index.html>`_, only instead of one of them.

Switching to Poetry
----------------------

If a project is currently on Pipenv or uv, switching back to Poetry converts its existing dependencies for you — nothing is lost, and nothing needs to be reinstalled by hand:

.. code-block:: bash

    appcraft add_template poetry

This reads whatever dependencies the project currently has and rewrites them as Poetry's ``[tool.poetry.*]`` tables in ``pyproject.toml``, removing the previous manager's files (a ``Pipfile``, for instance) in the process.
