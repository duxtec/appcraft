Presentation Layer
====================

The **Presentation Layer** is responsible for a specific way of exposing the application — the CLI today, or a web framework like Flask when that template is installed. It depends on the **Application Layer**'s use cases and schemas, and never the other way around.

What belongs here
------------------

- **CLI Presentations** (``presentation/cli/``) — formats use case output for the command line.
- **Web-facing input validation and exception translation**, when a web framework template is installed (``presentation/web/``).

What to avoid here
-------------------

- **Business logic.** The Presentation Layer displays data and captures input; it never decides what that data means.
- **Direct database access or persistence.** That's the **Application**/**Infrastructure** layers' job, reached only through a use case.
- **Heavy computation.** Presentation should stay cheap — formatting and validation, not processing.
- **Tight coupling to a specific framework's internals** beyond what's strictly needed to receive input and send output.

Naming convention: ``<Domain>CLIPresentation``
-------------------------------------------------

A CLI presentation is a class named ``<Domain>CLIPresentation``, constructed with the use case(s) it presents, with a nested ``class Printer(ComponentPrinter)`` (setting ``domain = "..."``) holding the actual ``@classmethod`` print methods. ``ComponentPrinter`` (``infrastructure/framework/appcraft/utils/component_printer.py``) wraps every print call to auto-translate its message when the ``locales`` template is installed — and is a no-op passthrough when it isn't, so a presentation class never needs to check for that itself.

Example: a CLI Presentation
------------------------------

``presentation/cli/app.py`` — every fresh project ships this one, backing the default ``runners/main/app.py`` runner:

.. code-block:: python

    from application.schemas.output.app import AppSchema
    from application.use_cases.app.get import GetAppUseCase
    from infrastructure.framework.appcraft.utils.component_printer import (
        ComponentPrinter,
    )


    class AppCLIPresentation:

        class Printer(ComponentPrinter):
            domain = "app"

            @classmethod
            def welcome(cls, app_name: str):
                message = cls.translate("Welcome to {app_name}")
                cls.title(message.format(app_name=app_name))

            @classmethod
            def app_info(cls, app: AppSchema):
                app_dict = app.model_dump()
                cls.title("App Informations")
                for name, value in app_dict.items():
                    cls.info(name, end=": ")
                    cls.print(value)

        def __init__(self, app_use_case: GetAppUseCase) -> None:
            self.app_use_case = app_use_case

        def show_informations(self) -> None:
            app = self.app_use_case.execute()
            self.Printer.app_info(app)

        def start(self) -> None:
            app = self.app_use_case.execute()
            self.Printer.welcome(app.name)

Each public method (``show_informations``, ``start``) follows the same shape: call the use case's ``execute()``, then hand the result to the ``Printer``. The ``Printer`` nested class never talks to the **Application Layer** directly — it only ever receives data that's already been through a use case and a schema.
