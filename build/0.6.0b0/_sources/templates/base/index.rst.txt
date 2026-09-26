Base Template
=============================

The **Base Template** is the foundation every project starts from — it's a `default template <../concepts/index.html#default-templates>`_, included automatically whether you name it or not. It provides the Clean Architecture layout (see `Layered Architecture <../../architecture/index.html>`_ for the internals), a working example (a ``User`` model with full CRUD), and the runtime that powers every other template.

A working project out of the box
------------------------------------

A fresh project isn't just an empty skeleton — it runs immediately:

- **A default in-memory database.** Every project starts with a zero-dependency, in-process database adapter, so the example ``User`` CRUD works without installing or configuring anything. Install `SQLAlchemy <../sqlalchemy/index.html>`_ or `MongoDB <../mongodb/index.html>`_ later to switch to a real one — the code that uses the database doesn't need to change.
- **A default package manager (Poetry).** Switch to `Pipenv <../pipenv/index.html>`_ or `uv <../uv/index.html>`_ any time — your existing dependencies convert automatically, nothing is lost. See `Exclusive Templates <../concepts/index.html#exclusive-templates>`_.
- **Central configuration** in ``config/app.toml`` — project name/version, environment, debug mode, log level, language, theme, and which database/package manager backs the generic defaults above.

Resilience and developer experience
---------------------------------------

- **Automatic recovery from missing dependencies.** If a runner hits an import error for a package that isn't installed yet, the framework installs it automatically (through whichever package manager the project is using) and retries — you don't need to stop and run an install command by hand.
- **Consistent, themeable CLI output** — a message printer with distinct styles for success, warning, error, critical, title, and info messages, so every template's output looks and feels consistent.
- **The runner system** — the interactive (or fully-scriptable) entry point every project uses to run its own code; see `Runner Layer <../../architecture/runner/index.html>`_ for how it works and how to add your own.

Learning the architecture by example
----------------------------------------

The generated ``User`` model, repository, use cases, and CLI presentation aren't just filler — they're a complete, working reference implementation of every layer described on the `Layered Architecture <../../architecture/index.html>`_ pages, worth reading through before building your own.
