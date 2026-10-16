GitHub Template
=============================

The **GitHub Template** lets a project create, delete and release repositories on `GitHub <https://github.com>`_. It's the GitHub adapter for the `Remote Repository Template <../remote_repository/index.html>`_, which provides the commands and does the work. This template adds only the GitHub-specific part. It depends on the Remote Repository Template, and through it on the `Git Template <../git/index.html>`_.

Requirements
---------------

The adapter uses the `GitHub CLI (gh) <https://cli.github.com/>`_, which must be installed and authenticated:

.. code-block:: bash

    gh auth login

If ``gh`` is missing or not logged in, the commands that talk to GitHub stop with a message saying so. In scripts, add ``interactive=false`` to every command, as the `Remote Repository Template <../remote_repository/index.html>`_ describes.

What it does
---------------

- **Creates repositories** with ``python tools remote_repository create_repo``, using the name, description and visibility you choose. The new repository becomes the local ``origin``.
- **Deletes repositories** with ``python tools remote_repository delete_repo``.
- **Publishes releases.** After ``python tools git release`` tags a version, a GitHub release is created for that tag. Pre-release versions (``0.7.0a1``, ``0.7.0b1``) are published as GitHub pre-releases.

It has no commands of its own; everything goes through the Remote Repository Template's runner.

Example
----------

.. code-block:: bash

    appcraft init github
    cd my-project
    python tools remote_repository create_repo
    python tools git release
