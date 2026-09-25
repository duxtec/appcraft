Runner Layer
====================

Runners are the entry points of the generated application — they bootstrap the process and call into the **Presentation Layer**. The runners you write live in ``runners/main/`` and ``runners/tools/`` — see `Types of runners`_ below.

What to Do in Runners
-------------------------

- **Keep them thin.** A runner method should build its dependencies (adapter, repository, use case, presentation) and call one presentation method — nothing more.
- **Wire dependencies explicitly.** Instantiate the concrete classes a runner needs directly (or via a ``Provider`` for interchangeable ones) — there's no dependency-injection container to configure.
- **One responsibility per method.** Each ``@Runner.runner``-decorated method should do one thing end to end.

What to Avoid in Runners
--------------------------

- **Business logic.** A runner orchestrates a call into **Presentation**; it never contains business rules or complex decision-making itself.
- **Heavy or long-running work inline**, beyond what the use case it calls already does — a runner is a thin entry point, not a place to implement additional processing.
- **``print()`` for output.** Use the **Presentation Layer**'s ``Printer``/``ComponentPrinter`` instead, so output stays consistent (and translatable) across the whole application.

Types of runners
-----------------

- **Main Runners** (``runners/main/``) — the primary entry points of the application, run via ``python run``.
- **Tool Runners** (``runners/tools/``) — secondary, dev/ops-style tasks (seeding data, running a benchmark, generating config), run via ``python run_tools``.

To define a class as a runner, it must:

- Live in either ``runners/main`` or ``runners/tools``.
- Inherit from ``Runner`` (``infrastructure.framework.appcraft.core.runner.Runner``).
- Mark the methods meant to be invokable with the ``@Runner.runner`` decorator — a method without it (e.g. a helper) is never shown as a selectable action.

Example of a Runner
-----------------------

``runners/main/app.py`` — every fresh project ships this one:

.. code-block:: python

    from application.use_cases.app.get import GetAppUseCase
    from infrastructure.framework.appcraft.app.provider import AppProvider
    from infrastructure.framework.appcraft.core.runner import Runner
    from presentation.cli.app import AppCLIPresentation


    class AppRunner(Runner):
        @Runner.runner
        def start(self):
            app_adapter = AppProvider()
            app_use_case = GetAppUseCase(app_provider=app_adapter)
            presentation = AppCLIPresentation(app_use_case=app_use_case)
            presentation.start()

        def non_runner1(self):
            # This method does not show in the runner menu —
            # it isn't decorated with @Runner.runner.
            pass

Running Applications
-------------------------

To execute the **Main runners** within your project, use:

.. code-block:: bash

    python run

This runs the main runner(s) located in ``runners/main``. If there's more than one candidate at any step, you'll be prompted to choose the file, class, and method interactively (this needs the ``prompt_toolkit`` template installed — without it, the full path must always be passed inline, as below).

Running Tool Runners
--------------------------------

To execute a **Tool Runner**, use:

.. code-block:: bash

    python run_tools

Same behavior as ``python run``, but scanning ``runners/tools`` instead of ``runners/main``.

Executing a Specific Runner
----------------------------------

You can always target a runner directly instead of going through the interactive menu:

.. code-block:: bash

    python run file_name class_name method_name

- ``file_name``: the module under ``runners/main`` (or ``runners/tools`` for ``python run_tools``) containing the runner class, without the ``.py`` extension.
- ``class_name``: the ``Runner`` subclass to use.
- ``method_name``: the ``@Runner.runner``-decorated method to call.

Any piece that has only one possible value can be omitted — if the target file has only one ``Runner`` subclass, ``class_name`` is inferred; if that class has only one runnable method, ``method_name`` is inferred too. In the smallest case, with exactly one file, one class, and one method, ``python run`` alone resolves everything automatically, with no prompt at all.

Any extra ``key=value`` arguments after the file/class/method are forwarded to the method as keyword arguments — e.g. ``python run flask Flask start port=8080``.
