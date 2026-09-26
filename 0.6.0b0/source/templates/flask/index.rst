Flask Template
=============================

The **Flask Template** is the `shared foundation <../concepts/index.html#shared-base-templates>`_ for building Flask applications — the application factory, routing, and project layout that both `Flask API <../flask_api/index.html>`_ and `Flask UI <../flask_ui/index.html>`_ build on. It can't be installed by itself; install one or both of those instead.

Automatic routing
--------------------

Routes and views don't need manual registration — drop a file in the right place and the Flask Template picks it up automatically:

- A ``Blueprint`` or ``register()`` function under ``presentation/web/api/v1/routes/`` (when ``flask_api`` is installed) is mounted under ``/api/v1``.
- A view function under ``presentation/web/ui/views/`` (when ``flask_ui`` is installed) becomes a URL rule.
- Every ``.html`` file under ``presentation/web/ui/templates/pages/`` (also ``flask_ui``) becomes a static route.

Database integration
------------------------

If `SQLAlchemy <../sqlalchemy/index.html>`_ is also installed, the Flask Template connects to it automatically on startup. Without it, the application still runs — just without persistence — rather than failing to start.

Development vs. production
------------------------------

By default, the application runs on Flask's own development server. Setting ``environment = "production"`` in ``config/app.toml`` switches it to **gunicorn** instead — a production-grade WSGI server — with no other changes needed. Either way, the server listens on port 5000 by default, overridable with the ``PORT`` environment variable.

This matters most in combination with the `Docker Template <../docker/index.html>`_: the same image works for local development and for a real deployment, just by changing that one configuration value before building.
