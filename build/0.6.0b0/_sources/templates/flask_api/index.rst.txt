Flask API Template
=============================

The **Flask API Template** adds a JSON API on top of the shared `Flask Template <../flask/index.html>`_ — it depends on ``flask`` and can be installed together with, or independently of, the `Flask UI Template <../flask_ui/index.html>`_.

It adds a versioned **presentation layer** for API endpoints under ``presentation/web/api/v1/`` (``routes/``, ``schemas/``, ``errors/``), which ``flask``'s own router auto-discovers and mounts under ``/api/v1`` — no manual registration needed. The ``errors/`` folder ships as scaffolding for you to fill in with project-specific error handling.

If the ``sqlalchemy`` template is also installed, the shared ``flask`` template initializes the database connection automatically; without it, the API runs without persistence.

This template doesn't ship any dependency of its own — its only requirement, the ``flask`` package itself, is declared by the shared ``flask`` template it depends on.
