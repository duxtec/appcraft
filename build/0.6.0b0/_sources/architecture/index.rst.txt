Layered Architecture
======================

Appcraft scaffolds projects around a **Clean Architecture** layout: each layer has one responsibility and depends only on the layers "beneath" it, never the other way around. This keeps business rules independent of frameworks, databases, and delivery mechanisms, so any of those can change without rippling through the rest of the codebase.

The layers, from the outside in:

1. **Runner**: the entry points of the generated application. A runner receives command-line input and calls into the **Presentation** layer.
2. **Presentation**: input validation, output formatting, and error translation for a specific delivery mechanism (CLI today, or a web framework like Flask). It depends on the **Application** layer.
3. **Application**: orchestrates business logic — use cases, repositories, ports, mappers, providers, schemas. It depends only on the **Domain** layer.
4. **Domain**: the core business entities, value objects, and abstract contracts (interfaces, filters). It has no framework or infrastructure dependencies at all.
5. **Infrastructure**: concrete implementations — database adapters, third-party API clients, the framework's own runtime utilities. It implements the contracts the **Domain** and **Application** layers define.

Dependencies only ever point inward (Runner → Presentation → Application → Domain), with **Infrastructure** implementing contracts defined by the layers it supports rather than being depended on directly by **Domain** or **Application** business logic.

.. toctree::
   :maxdepth: 2
   :caption: Architecture Layers

   runner/index
   presentation/index
   application/index
   domain/index
   infrastructure/index

.. toctree::
   :maxdepth: 2
   :caption: Application flow

   flow/index
