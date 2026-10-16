Remote Repository Template
=============================

The **Remote Repository Template** is the shared foundation for hosting a project on a remote Git platform. It can't be installed by itself (``standalone = False``): install the `GitHub Template <../github/index.html>`_ instead, which depends on this one. It also depends on the `Git Template <../git/index.html>`_.

It provides three things, none of them tied to one platform:

- **A generic runner**, with ``create_repo`` and ``delete_repo``, that works with whichever platform is installed.
- **A platform-agnostic contract** (``RemoteRepositoryPort``) that every platform adapter implements: create, look up and delete repositories, and create releases.
- **A provider** that picks the platform to use when more than one is installed.

Commands
-----------

.. code-block:: bash

    python tools remote_repository create_repo
    python tools remote_repository delete_repo

``create_repo`` asks for the repository name, description and visibility (or accepts them as arguments), creates it on the platform and points the local ``origin`` remote at it, pushing every branch.

``delete_repo`` is destructive and can't be undone, so it shows a warning and asks you to type the repository's exact name. Anything else aborts without touching the platform. Automation passes the name again with ``confirm_name``, which must match ``name``:

.. code-block:: bash

    python tools remote_repository delete_repo name=my-project confirm_name=my-project

In scripts and CI, add ``interactive=false``: a missing argument then stops the run with an error instead of waiting for an answer.

Choosing the platform
------------------------

``config/remote_repository.toml`` sets the platform to use by default:

.. code-block:: toml

    default_platform = "github"

``github`` is the only platform available right now. The setting only matters when several platforms are installed.

Adding a platform
--------------------

A new platform (GitLab, Bitbucket, ...) is a template that depends on this one and contributes only its own adapter. Nothing in this template needs to change.
