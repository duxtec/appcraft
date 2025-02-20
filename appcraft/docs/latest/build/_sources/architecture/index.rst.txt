Layered Architecture
======================

In this section, we introduce the **Layered Architecture** of the AppCraft framework. The architecture follows a clean and modular design, ensuring flexibility and scalability. The system is divided into multiple layers, each with distinct responsibilities, allowing for easy maintainability and extensibility.

The architecture layers are:

1. **Runner**: The entry points of the application. It initiates the process and calls the **Presentation** layer or **Service** layer.
2. **Presentation**: This layer handles the user interface and presentation logic. It interacts with the **Application** layer to present data to the user.
3. **Application**: Manages interactions between the **Presentation** layer and the **Domain** layer. It handles business logic and operations, such as calling models from the **Domain** and managing adapters and frameworks from the **Infrastructure**.
4. **Domain**: Represents the core business entities. This layer contains the application's data models and business rules.
5. **Infrastructure**: Includes all the external systems, frameworks, and adapters, such as databases, third-party services, file management, and more.

.. toctree::
   :maxdepth: 2
   :caption: Architecture Layers

   runner/index
   presentation/index
   application/index
   domain/index
   infrastructure/index

