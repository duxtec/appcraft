Presentation Layer
==================

The **Presentation Layer** is responsible for handling user interactions and presenting the data. It is designed to separate the user interface (UI) concerns from the core business logic and other layers of the application.

In this layer, you'll typically find different components responsible for displaying information to the user and capturing their inputs.

The Presentation Layer is mainly composed of the following:

    1. **CLI Presentations**:
        Handle the command-line interface (CLI) interactions.
        
    2. **UI Presentations**:
        Manage user interfaces (like web or graphical UIs), though this is an optional component depending on the type of application you're building.

Here's a refined section on "What to Avoid in Presentation" for your documentation:

What to Do in Presentation
---------------------------------

    - **Follow the Dependency Inversion Principle**:
        The Presentation Layer should depend on the **Application Layer**, not on **Infrastructure** or **Domain** directly. It should communicate only through services or use cases.

    - **Use DTOs for Data Transfer**:
        Always use **DTOs (Data Transfer Objects)** to structure incoming and outgoing data. This ensures that the Presentation Layer does not work directly with **Domain Models**, reducing coupling.

    - **Validate User Input**:
        Validate all incoming data before passing it to the **Application Layer**. This prevents invalid or incomplete data from reaching business logic and causing errors.

    - **Keep Controllers Lightweight**:
        Controllers (or handlers) should only be responsible for handling requests, calling **Application Services**, and returning responses. Business logic should never be in controllers.

    - **Implement Proper Error Handling**:
        Capture and format errors in the Presentation Layer before sending responses. Use proper HTTP status codes in APIs and meaningful messages in UI or CLI applications.

    - **Ensure Idempotency in APIs**:
        If exposing an API, ensure that **POST, PUT, and DELETE** operations are idempotent when necessary, avoiding unintended duplicate operations.

    - **Decouple from the Framework**:
        The Presentation Layer should not be tightly coupled to any specific framework. Keeping it loosely coupled makes it easier to change frameworks if needed.

    - **Use a Consistent Response Format**:
        Define and follow a **structured response format** for all API endpoints. This makes it easier to integrate with clients.

    - **Apply Authentication and Authorization**:
        Ensure that API endpoints and UI actions are properly secured using authentication and authorization mechanisms before calling business logic.

What to Avoid in Presentation
--------------------------------
In the **Presentation Layer**, it is crucial to maintain a clear separation of concerns. Here are some common pitfalls to avoid:

    - **Avoid Business Logic in Presentation Layer**:
        Do not include any business logic or complex decision-making processes in the Presentation Layer. This logic should reside in the **Application Layer** or the **Domain Layer**. The Presentation Layer should only be responsible for presenting data to the user and handling user input.
    
    - **Avoid Direct Database Access**:
        Avoid direct interaction with the database in the Presentation Layer. Database access and data manipulation should be handled by the **Application Layer** via services or repositories.
    
    - **Avoid Heavy Computation in Presentation Layer**:
        Avoid heavy computations in the **Presentation Layer**. The **Presentation Layer** should focus on displaying the data and not processing large datasets or performing calculations. These tasks should be delegated to the **Application** or **Domain** layers.
    
    - **Avoid Side Effects in Presentation Layer**:
        The **Presentation Layer** should avoid making changes to the system state, such as saving data to the database or triggering external actions. Instead, it should communicate with the **Application Layer** to handle such side effects.
    
    - **Avoid Logging and Debugging in Presentation Layer**:
        Avoid placing logging or debugging statements in the **Presentation Layer**. Logs should be handled at the **Service** or **Domain** levels, not in the UI or presentation code.
    
    - **Avoid Tightly Coupled Components**:
        The **Presentation Layer** should not be tightly coupled to the specific implementation details of the **Domain** or **Infrastructure** layers. It should rely on abstractions such as interfaces or services to interact with the underlying layers.

This section ensures that the **Presentation Layer** stays focused on what it's meant to do—displaying data and handling user interaction—while keeping other responsibilities in the appropriate layers.

Example of a CLI Presentation
------------------------------

Below is an example of a class that demonstrates the **CLI Presentation** using the `AppCLIPresentation` class:

.. code-block:: python

    from application.dtos.app_dto import AppDTO
    from application.services.app_service import AppService
    from infrastructure.framework.appcraft.utils.component_printer \
        import ComponentPrinter


    class AppCLIPresentation:

        class Printer(ComponentPrinter):
            domain = "app"

            @classmethod
            def welcome(cls, app_name: str):
                message = cls.translate("Welcome to {app_name}")
                cls.title(message.format(app_name=app_name))

            @classmethod
            def app_info(cls, app: AppDTO):
                app_dict = app.to_dict()
                cls.title("App Informations")
                for name, value in app_dict.items():
                    cls.info(name, end=": ")
                    cls.print(value)

        def __init__(self, app_service: AppService) -> None:
            self.app_service = app_service

        def show_informations(self) -> None:
            app = self.app_service.get_app()
            self.Printer.app_info(app)

        def start(self) -> None:
            app = self.app_service.get_app()
            self.Printer.welcome(app.name)


In this example:

- `AppCLIPresentation` is a class responsible for presenting the application information in a command-line interface.
- `Printer` is a nested class that extends `ComponentPrinter` and contains methods to display different pieces of information (like `welcome()` and `app_info()`).
- `show_informations()` calls the `app_info()` method to display detailed information about the app, such as name, version, environment, etc.
- `start()` displays a welcome message with the app's name.

This is just one of the ways to implement the Presentation Layer, and you can expand it based on your project's needs. The Presentation Layer can be used for both presenting data and handling interactions, with flexibility for your particular application.
