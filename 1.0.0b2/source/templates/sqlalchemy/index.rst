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

Runners
----------

The SQLAlchemy Template ships one runner, in ``runners/main/database.py``, that inspects the connected database:

- ``python run database show_tables`` lists every table, with its columns and their types.
- ``python run database show_columns table=users`` shows the columns of one table (here, the example ``users`` table). Without ``table``, it falls back to listing every table.

Adding a Table for a New Model
------------------------------

Once a model is stored in the database, the adapter needs an ORM class for it. The adapter finds that class by name, so the ORM class must have **the same name** as the domain model. For the ``Product`` model from :doc:`../../developing/recipes`, create ``infrastructure/database/sqlalchemy/models/product.py``:

.. code-block:: python

    from sqlalchemy import Column, String

    from infrastructure.database.sqlalchemy.models.base import Base


    class Product(Base):
        __tablename__ = "products"

        name = Column(String, nullable=False)

        def __init__(self, name: str):
            self.name = name

``Base`` already provides the ``id``, ``created_at`` and ``updated_at`` columns, so only your own columns go here.

Tables are created only when the database has no tables at all. A model added to a database that already has tables, such as the example ``users`` table, gets no table automatically, and saving to it fails with ``no such table``. Create the missing tables with a tools runner, for example ``runners/tools/tables.py``:

.. code-block:: python

    from infrastructure.database.sqlalchemy.adapter import get_sqlalchemy_adapter
    from infrastructure.core.runner import Runner


    class Tables(Runner):
        @Runner.runner
        def create(self):
            get_sqlalchemy_adapter().create_all()

.. code-block:: bash

    python tools tables Tables create

``create_all()`` creates the tables that are missing and leaves existing ones unchanged. It does not add a column to a table that already exists: this template ships no migration tool, so a change to an existing table has to be applied to the database by hand.

