Developing Your Project
=======================

This guide picks up where :doc:`../getting_started` stops. You have run ``appc init``, you have a project folder, and now you want to add your own features. It shows the day-to-day work inside a generated project: running commands, adding a command, adding a model, adding an operation, and deciding which folder a new piece of code belongs in.

Template-specific work, such as adding a Flask route or a database table, is covered on that template's own page. This guide links to them where they apply.

Your First Run
--------------

Start from a project with the ``base`` template (``appc init`` always includes it). The project ships with a small ``app`` runner you can use to see the flow end to end:

.. code-block:: bash

    python run app AppRunner start

``python run`` opens an interactive menu that lists the runners it finds in ``runners/main/``. Any runner can also be called directly, by file, class and method:

.. code-block:: bash

    python run <file> <class> <method> [key=value ...]

Everything after the method name is passed to it as keyword arguments. Use ``python tools`` in the same way for the runners in ``runners/tools/`` (maintenance tasks such as seeding data or generating files).

.. note::

    ``appc run ...`` and ``appc tools ...`` are the same as ``python run ...`` and ``python tools ...``, run from the project folder.

The Mental Model
----------------

Every feature follows the same path through the project:

.. code-block:: text

    runner  ->  presentation  ->  use case  ->  repository  ->  adapter (database, memory, ...)
                                      |
                                      v
                                   domain (models, value objects, filters)

- A **runner** is the entry point: it is what you call from the command line. It builds the objects it needs and calls one presentation method.
- A **presentation** class turns input into a use case call, and prints the result with a ``Printer``.
- A **use case** holds one business operation, such as "create a user". It is the only place that decides what happens.
- A **repository** is the application's view of one model: it reads and writes through a port.
- An **adapter** is the concrete storage behind a port. The default one keeps data in memory; installing a database template swaps in a real one.
- The **domain** holds the models and value objects that every other layer shares. It has no dependency on the framework or on storage.

Each layer has a folder with the same name (``runners/``, ``presentation/``, ``application/``, ``domain/``, ``infrastructure/``). See :doc:`../architecture/index` for the rules each layer follows.

Which Folder Does a New Piece Go In?
------------------------------------

Use this table to pick the folder before you write anything:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - You want to...
     - Put it in
   * - Add a command that someone runs from the terminal
     - A runner in ``runners/main/`` (application) or ``runners/tools/`` (maintenance). Recipe: :doc:`recipes` - *Add a runner*.
   * - Show or read input for a command
     - A presentation class in ``presentation/cli/``. Recipe: :doc:`recipes` - *Add a presentation class*.
   * - Add a business operation (create, list, change something)
     - A use case in ``application/use_cases/<concept>/``. Recipe: :doc:`recipes` - *Add a use case*.
   * - Add a new kind of data with fields
     - A model in ``domain/models/<name>.py``. Recipe: :doc:`recipes` - *Add a model*.
   * - Store and load a model
     - A repository in ``application/repositories/<name>.py``. Recipe: :doc:`recipes` - *Add a repository*.
   * - Add an HTTP endpoint
     - Flask template only: see :doc:`../templates/flask_api/index`.
   * - Add a web page
     - Flask UI template only: see :doc:`../templates/flask_ui/index`.
   * - Add a database table for a model
     - SQLAlchemy template only: see :doc:`../templates/sqlalchemy/index`.
   * - Connect to a new external service (a different database, an API client, a browser)
     - Infrastructure. This is rare. Most projects never need it. See the note below.

Work from the top of the table to the bottom when you add a feature: the runner calls the presentation, the presentation calls the use case, and the use case uses the repository. Each step only depends on the one below it.

.. note::

    Infrastructure is the layer you touch least. A new adapter is only needed when you want a storage or service that no installed template provides. Before writing one, check whether a template already ships an adapter for the same port (for example, ``sqlalchemy`` or ``mongodb`` for the database). Installing that template is usually enough.

Configuration
-------------

Settings live in ``config/`` as TOML files. Read them with ``Config`` instead of hard-coding values:

.. code-block:: python

    from infrastructure.core.config import Config

    app_config = Config().get("app")
    debug = app_config.get("debug_mode")

``config/app.toml`` is written by the ``base`` template. The keys you will most often read or change are:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Key
     - Meaning
   * - ``name``
     - The project name shown by the ``app`` runner.
   * - ``environment``
     - ``development`` or ``production``. Some templates change behavior with it, for example Flask uses gunicorn in production.
   * - ``debug_mode``
     - Turns debug output on or off.
   * - ``log_level``
     - ``debug``, ``info``, ``warning``, ``error`` or ``critical``.
   * - ``lang``, ``lang_preference``, ``supported_langs``
     - Language for the messages the framework prints.
   * - ``theme``
     - ``dark`` or ``light``.
   * - ``manager``
     - The package manager that owns the project's dependencies: ``poetry``, ``pipenv``, ``uv`` or ``pip``.
   * - ``default_database_adapter``
     - Which database backend to use when more than one is installed: ``sqlalchemy`` or ``mongodb``.

Other templates add their own file, for example ``config/database.toml`` (SQLAlchemy) or ``config/web_scraping.toml`` (web scraping). Their own pages list the keys they use.

Interactive and Non-Interactive Runs
------------------------------------

Runs are interactive by default. If an argument is missing, the runner asks for it. Pass ``interactive=false`` when the command runs from a script or CI:

.. code-block:: bash

    python run user UserRunner create interactive=false

With ``interactive=false``, a missing or invalid argument is an error. The message names the argument and the command exits with status 1:

.. code-block:: text

    Missing argument 'username'. Pass it as username=<value>.

Confirmations, such as deleting data, take their default when ``interactive=false`` is set. Your own runners get this behavior for free if you ask every question through ``read_input`` (see :doc:`recipes`).

Checking Your Work
------------------

The generated project does not ship with an automated test suite. Two quick checks cover most day-to-day changes:

- **Run the command.** Call the runner with real arguments, as in the recipes. This exercises the whole path, from runner to adapter.
- **Use Flask's test client** for web code. This checks a route without starting a server:

  .. code-block:: python

      from infrastructure.framework.flask.app import FlaskApp

      client = FlaskApp().app.test_client()
      response = client.get("/api/v1/ping")
      print(response.status_code, response.get_json())

Glossary
--------

Runner
    A class that subclasses ``Runner`` and has methods marked with ``@Runner.runner``. Each marked method is one command.

Presentation
    The class that turns runner input into a use case call and prints the result. The CLI version is named ``<Domain>CLIPresentation``.

Printer
    A nested ``ComponentPrinter`` class inside a presentation. It holds the messages the presentation prints, so output stays consistent.

Use case
    One business operation with an ``execute()`` method. Named ``<Action>UseCase``, for example ``CreateUserUseCase``.

Model
    A domain entity, such as ``User``. A ``New<Model>`` class (for example ``NewUser``) holds the data before it has an id.

Schema
    A data shape for input or output, under ``application/schemas/``. Use cases take input schemas and return output schemas.

Repository
    The application class that reads and writes one model through a port.

Port
    An abstract contract the application depends on, such as ``DatabasePort``.

Adapter
    A concrete implementation of a port, such as ``MemoryAdapter`` or ``SQLAlchemyAdapter``.

Provider
    A function that picks which adapter to use at runtime, based on the installed templates. For example, ``get_default_database_adapter()``.

Template
    A composable set of files and dependencies that is added to the project with ``appc init`` or ``appc add_template``.

.. toctree::
   :maxdepth: 1
   :hidden:

   recipes
