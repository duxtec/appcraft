MongoDB Template
====================

The **MongoDB Template** provides a ``DatabasePort`` adapter backed by **MongoDB** (via ``pymongo``), giving your project document storage instead of the zero-dependency, in-memory storage every fresh project starts with.

It's an `interchangeable template <../concepts/index.html#interchangeable-templates>`_: install it on its own to replace the in-memory default, or alongside `SQLAlchemy <../sqlalchemy/index.html>`_ — ``config/app.toml``'s ``default_database_adapter`` picks which one backs the generic default when both are installed, and code that specifically wants document storage can use MongoDB directly regardless of that setting.

What it adds
--------------

- A MongoDB connection, configured through its own ``config/mongodb.toml``.
- Filter translation so the domain's engine-agnostic filters (``EqualFilter``, ``LikeFilter``, ...) work against MongoDB queries.
- A demo domain model (``Programmer``) with a seeding tool — ``python run_tools programmers`` — to see document storage in action right away, separate from the generic ``User`` model the ``base`` template ships.
