Domain Layer
=============
The **Domain Layer** is the heart of your application, where the business logic and rules are defined. It contains the **models** that represent your business entities, and the **infrastructure interfaces** that define the contract for persisting and retrieving these entities. This layer is independent of any external concerns, such as databases or frameworks, and focuses solely on the core logic of the application.

The Domain Layer serves to encapsulate the business rules and logic, ensuring that the rest of the system can interact with it without knowing the underlying implementation details.

What to Do in Domain  
--------------------------------  
In the **Domain Layer**, it is essential to follow best practices to ensure a clean, maintainable, and scalable architecture. Here are some key principles to follow:  

- **Encapsulate Business Logic**:  
  The Domain Layer should be the central place for business rules and domain logic. Keep this layer independent of external frameworks or infrastructure to ensure testability and reusability.  

- **Use Rich Domain Models**:  
  Prefer using rich domain models that encapsulate both data and behavior instead of relying only on anemic data structures. This helps enforce domain rules and improves maintainability.  

- **Keep Domain Models Independent**:  
  Avoid dependencies on infrastructure, frameworks, or database models. The domain models should represent the business concepts without being affected by external concerns.  

- **Define Clear Boundaries**:  
  Clearly define the boundaries of your domain entities and value objects. Ensure that changes to one entity do not inadvertently impact unrelated parts of the system.  

- **Follow Interface-Based Design for Repositories**:  
  Define repository interfaces in the Domain Layer, keeping the implementation details in the Infrastructure Layer. This abstraction allows easy substitution and testing.  

- **Use Value Objects When Applicable**:  
  Instead of using primitive types everywhere, consider using **Value Objects** for attributes that have specific business meaning, ensuring data consistency and enforcing constraints.  

- **Ensure Immutability When Possible**:  
  Make domain models immutable whenever possible to prevent unintended side effects and maintain a predictable state throughout the application.  

- **Write Unit Tests for Domain Logic**:  
  The Domain Layer should be highly testable. Write unit tests to verify business rules and domain logic independently from external dependencies.  

What to Avoid in Domain
------------------------
In the **Domain Layer**, it is crucial to maintain a clear separation of concerns. Here are some common pitfalls to avoid:

    - **Business Logic in Other Layers**: Avoid placing business logic in the **Application Layer**, **Presentation Layer**, or **Infrastructure Layer**. The **Domain Layer** should be the place for business rules and models.
    
    - **Direct Database Access**: Avoid having database-specific code or direct access to databases in the **Domain Layer**. Use repository interfaces to abstract away the database interaction.
    
    - **External Dependencies**: The **Domain Layer** should not have dependencies on external frameworks, libraries, or infrastructure concerns. Keep it focused on the core business logic and rules.
    
    - **UI Logic**: Avoid placing UI-related logic in the **Domain Layer**. The **Domain** should be agnostic to the user interface and should not know how data is presented to the user.
    
    - **Global State**: The **Domain Layer** should not depend on or modify global state. The state should be encapsulated in objects and managed through domain logic.

Example of a Model
------------------
Here's an example of a **Model** in the **Domain Layer**, representing a **User**:

.. code-block:: python

    # domain/models/user.py
    class User:
        def __init__(self, user_id: int, name: str, email: str):
            self.user_id = user_id
            self.name = name
            self.email = email

        def change_name(self, new_name: str):
            self.name = new_name

        def change_email(self, new_email: str):
            self.email = new_email

        def __repr__(self):
            return f"User(id={self.user_id}, name={self.name}, email={self.email})"

In this example, the `User` class is a core business model that represents a user entity. It encapsulates the data and behaviors related to a user in the system.

Example of Repository Interface
--------------------------------
Here's an example of a **Repository Interface** in the **Domain Layer**, defining methods for interacting with **User** data:

.. code-block:: python

    # domain/repositories/user_repository_interface.py
    from abc import ABC, abstractmethod
    from domain.models.user import User

    class UserRepositoryInterface(ABC):
        @abstractmethod
        def get_by_id(self, user_id: int) -> User:
            """Retrieve a user by ID"""
            pass

        @abstractmethod
        def create(self, user: User) -> None:
            """Create a new user"""
            pass

        @abstractmethod
        def update(self, user: User) -> None:
            """Update an existing user"""
            pass

        @abstractmethod
        def delete(self, user: User) -> None:
            """Delete a user"""
            pass

In this example, the `UserRepositoryInterface` defines the contract for repository operations such as creating, updating, and deleting users. This repository is abstract and doesn't deal with database specifics—it only specifies what actions can be performed on the **User** entity.

Example of Adapter Interface
--------------------------------
This is an example of an **Adapter Interface** in the **Domain Layer**, defining a contract for retrieving **App** data:

.. code-block:: python

    # domain/adapters/app_adapter_interface.py
    from abc import ABC, abstractmethod

    from domain.models.app import App


    class AppAdapterInterface(ABC):
        @abstractmethod
        def get_app(self) -> App:
            pass

In this example, the `AppAdapterInterface` establishes a clear contract for accessing application-related data.
This interface does not deal with infrastructure-specific details (such as databases, filesystem or external APIs); instead, it defines the expected behavior that any concrete adapter must implement.
By using this abstraction, the **Application Layer** can interact with the infrastructure in a decoupled manner, ensuring better maintainability and testability.