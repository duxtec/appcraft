SQLAlchemy Template
=============================

The **SQLAlchemy Template** provides a ``DatabasePort`` adapter backed by **SQLAlchemy**, giving your project a real relational database connection instead of the zero-dependency, in-memory storage every fresh project starts with.

It's an `interchangeable template <../concepts/index.html#interchangeable-templates>`_: install it on its own to replace the in-memory default, or alongside `MongoDB <../mongodb/index.html>`_ — ``config/app.toml``'s ``default_database_adapter`` picks which one backs the generic default when both are installed, and code that specifically wants SQLAlchemy can use it directly regardless of that setting.

What it adds
--------------

- A real database connection, configured through its own ``config/database.toml`` (connection string, pool settings).
- ORM models and filter translation so the domain's engine-agnostic filters (``EqualFilter``, ``LikeFilter``, ...) work against a real SQL database.
- Introspection tools: ``python run database`` lists tables and columns of the connected database.

Combining with Flask
-----------------------

If the `Flask Template <../flask/index.html>`_ (or ``flask_api``/``flask_ui``) is also installed, it detects SQLAlchemy automatically and wires up the database connection for you — no extra configuration needed. Without SQLAlchemy, a Flask-based project still runs fine, just without persistence.
