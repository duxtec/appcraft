Docker Template
=============================

The **Docker Template** containerizes the generated project — a single ``Dockerfile`` plus a ``docker-compose.yml`` generated automatically from whatever else is installed.

Dynamic, one service per entry point
----------------------------------------

Right after install, and again whenever you ask it to, this template scans ``runners/main`` for every ``Runner`` that exposes a ``start`` action and writes one ``docker-compose.yml`` service per match — the CLI's own runner, a Flask app if installed, and so on. Install just the CLI and you get one service; add ``flask_api`` and a ``flask`` service appears too, with no manual compose editing.

If you install a new ``runners/main`` template later, refresh the compose file explicitly:

.. code-block:: bash

    python run_tools docker generate_compose

This is a full rewrite of the file, so back up any manual edits (ports, volumes, environment variables) first — it isn't run automatically on every unrelated template install specifically so those edits aren't clobbered without warning.

Building and running
------------------------

Everything routes through the project root — no need to ``cd`` into ``infrastructure/docker`` first:

.. code-block:: bash

    python run_tools docker build [service=<name>]
    python run_tools docker up [service=<name>]
    python run_tools docker down

Omit ``service`` to act on every service in the compose file. These wrap the ``docker compose`` CLI (falling back to the standalone ``docker-compose`` v1 binary if the modern plugin isn't installed).

No hardcoded package manager
--------------------------------

The image installs dependencies through whichever of `Poetry <../poetry/index.html>`_, `Pipenv <../pipenv/index.html>`_, or `uv <../uv/index.html>`_ your project is actually using — no changes needed if you switch package managers later. It also runs as a non-root user.

Development vs. production
------------------------------

The image always installs your project's real dependencies, but skips dev-only tooling (linters, doc builders) when ``config/app.toml``'s ``environment`` is set to ``"production"`` — set that *before* building for a real deployment. If the `Flask Template <../flask/index.html>`_ is installed, this same setting also switches its runner from the development server to a production-grade one — see `Flask <../flask/index.html#development-vs-production>`_.

One thing to set up yourself
--------------------------------

The generated ``docker-compose.yml`` doesn't guess exposed ports, since that's specific to how you're actually deploying. Add a ``ports:`` entry to a service if you need to reach it from outside the container, e.g.:

.. code-block:: yaml

    services:
      flask:
        ports:
          - "5000:5000"
