Application Layer
=================

The **Application Layer** is responsible for orchestrating business logic within the application. It sits between the **Presentation Layer** and the **Domain Layer**, handling the flow of data and ensuring that all interactions between the different layers are seamless. This layer often contains **Services**, **DTOs** (Data Transfer Objects), **Mappers**, and sometimes **Use Cases**. 

The **Application Layer** coordinates the actions of the **Domain Layer** by interacting with models, repositories, and services, and it prepares the data to be sent to the **Presentation Layer**.

Aqui está a seção **"What to Do in Application"**, seguindo o mesmo formato da **"What to Avoid in Application"**:  

What to Do in Application  
--------------------------------  
In the **Application Layer**, it is essential to follow best practices to ensure the proper orchestration of business logic and system interactions. Here are some key principles to follow:  

- **Orchestrate Business Logic, Do Not Implement It**:  
  The **Application Layer** should coordinate interactions between the **Domain Layer** and external layers. Avoid implementing business rules here; instead, delegate them to the **Domain Layer**.  

- **Use DTOs for Data Transfer**:  
  Introduce **Data Transfer Objects (DTOs)** to shape the data exchanged between the **Application Layer** and **Presentation Layer**, ensuring separation of concerns and avoiding unnecessary dependencies on domain models.  

- **Implement Application Services**:  
  Keep application logic within well-defined **Application Services**, ensuring that use cases are clearly implemented and reusable. These services should act as intermediaries between the **Presentation Layer** and the **Domain Layer**.  

- **Leverage Mappers for Data Transformation**:  
  Use **Mappers** to convert data between **DTOs** and **Domain Models**. This ensures each layer remains independent and prevents unnecessary coupling.  

- **Enforce Transaction Boundaries**:  
  If an application service involves multiple repository calls, ensure that transactions are properly managed to maintain data consistency.  

- **Keep Dependencies on External Layers Minimal**:  
  The **Application Layer** should depend on the **Domain Layer** but should not have direct dependencies on external frameworks or infrastructure. Use dependency injection to manage dependencies effectively.  

- **Ensure Idempotency for Application Services**:  
  Application services should be designed to handle duplicate requests safely and prevent unintended side effects.  

- **Write Unit and Integration Tests**:  
  The **Application Layer** should be well-tested, covering different scenarios for service orchestration, data transformation, and interactions with the **Domain Layer**.  

What to Avoid in Application
---------------------------------

While working within the **Application Layer**, it's important to adhere to the following guidelines to ensure a clean and maintainable architecture. Here are some common practices to avoid:

- **Avoid Business Logic in Application Layer**:
    The **Application Layer** should not contain complex business logic. Business rules, validations, and domain-specific logic should reside in the **Domain Layer**. The Application Layer is responsible for orchestrating the flow of data and calls to other layers, not for implementing business rules.

- **Avoid Direct Interaction with Presentation Layer**:
    The **Application Layer** should never interact directly with the **Presentation Layer**. Its responsibility is to handle the orchestration of processes and provide data to be presented by the Presentation Layer. The Application Layer should not be concerned with rendering data or user-facing interactions.

- **Avoid Data Formatting or Rendering**:
    The **Application Layer** should not be responsible for formatting data, rendering views, or handling any user-facing interactions. This is the responsibility of the **Presentation Layer**. The Application Layer should focus on managing application flow and communicating with the **Domain Layer** and other necessary components.

- **Avoid Persistence Operations in Application Layer**:
    The **Application Layer** should not directly handle data persistence or database interactions. These tasks should be delegated to the **Domain Layer** or **Infrastructure Layer**, ensuring that the Application Layer remains focused on its orchestration role.

- **Avoid Tightly Coupled Components**:
    Avoid tightly coupling the **Application Layer** to the **Presentation Layer** or the **Infrastructure Layer**. The Application Layer should rely on abstractions and interfaces to communicate with other layers. This promotes flexibility, testability, and separation of concerns.

By adhering to these practices, the **Application Layer** remains focused on its core responsibility—managing application flow—while ensuring that other concerns, like business logic and presentation, are handled in the appropriate layers.

Example of a DTO
----------------

A **DTO** (Data Transfer Object) is a simple object used to transfer data between the **Application** and **Presentation Layers**. It is often used to simplify complex domain models and provide data in a form that is easy to transfer over a network or display in a user interface.

Here's an example of a DTO:

.. code-block:: python

    class AppDTO:
        def __init__(
            self, name: str, version: str,
            environment: str, debug_mode: bool
        ):
            self.name = name
            self.version = version
            self.environment = environment
            self.debug_mode = debug_mode

        def to_dict(self):
            return {
                "name": self.name,
                "version": self.version,
                "environment": self.environment,
                "debug_mode": self.debug_mode
            }


In this example, the `AppDTO` class is used to structure the application data in a way that can be easily transferred to the **Presentation Layer**.

Example of a Mapper
--------------------

A **Mapper** is responsible for converting between different types of objects or data structures. In the context of the **Application Layer**, a mapper is used to convert **Domain** models to **DTOs** and vice versa.

Here is an example of a Mapper that converts a `Domain` model to a `DTO`:

.. code-block:: python

    from application.dtos.app_dto import AppDTO
    from domain.models.app import App


    class AppMapper:
        @staticmethod
        def to_dto(app: App):
            return AppDTO(
                name=app.name,
                version=app.version,
                environment=app.environment,
                debug_mode=app.debug_mode,
            )

        @staticmethod
        def to_domain(app_dto: AppDTO):
            return App(
                name=app_dto.name,
                version=app_dto.version,
                environment=app_dto.environment,
                debug_mode=app_dto.debug_mode
            )


In this example, the `AppMapper` class defines methods for converting between the **Domain** model `App` and the **DTO** `AppDTO`. This separation allows for cleaner code and better maintainability.

Example of a Service
---------------------

A **Service** in the **Application Layer** is responsible for executing business logic and coordinating operations between the **Domain** and **Presentation** layers. A **Service** typically calls the **Domain Layer** to retrieve or manipulate data and then formats the data for the **Presentation Layer**.

Here's an example of an **Application Service**:

.. code-block:: python

    from application.dtos.app_dto import AppDTO
    from application.mappers.app_mapper import AppMapper
    from domain.interfaces.adapters.app_adapter_interface import (
        AppAdapterInterface,
    )


    class AppService:
        def __init__(self, app_adapter: AppAdapterInterface):
            self.adapter = app_adapter

        def get_app(self) -> AppDTO:
            app = self.adapter.get_app()
            app_dto = AppMapper.to_dto(app)
            return app_dto



Aqui está a explicação ajustada para refletir corretamente o fluxo de dados no exemplo:  

---

In this example, the `AppService` is responsible for retrieving application information through the `AppAdapterInterface`, which abstracts the infrastructure details.
The retrieved `App` object belongs to the **Domain Layer**.
To ensure a proper separation of concerns, the service uses the `AppMapper` to convert the domain model into an `AppDTO`, which is specifically designed for communication with the **Presentation Layer**.
By doing so, `AppService` acts as an intermediary, orchestrating data transformation and enforcing business rules **between the Domain and Presentation layers**, while keeping the infrastructure details decoupled.