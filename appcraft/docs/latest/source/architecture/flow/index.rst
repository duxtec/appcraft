.. _application_flow:

===================
Application Flow
===================

This document describes the request and response flow in the application, ensuring a clear separation of concerns and proper layer responsibilities.

Request Flow
============

1. **Runner (entrypoint)** → Instantiates the application layers.
2. **Presentation** → Receives user input, converts it into DTO + Filters.
3. **Mapper (Application)** → Converts DTO to Domain Model.
4. **Service (Application)** → Applies business rules, working with Domain Model.
5. **Repository (Agnostic)** → Sends Domain Model to the data layer.
6. **Adapter (Infrastructure)** → Interacts with the database and returns the Infrastructure Model.

Response Flow
=============

1. **Adapter (Infrastructure)** → Returns the Infrastructure Model.
2. **Mapper (Infrastructure)** → Converts Infrastructure Model to Domain Model.
3. **Repository (Agnostic)** → Returns the Domain Model.
4. **Service (Application)** → Applies business rules, returning the Domain Model.
5. **Mapper (Application)** → Converts Domain Model to DTO.
6. **Presentation** → Prepares the API response.

This architecture ensures full decoupling between layers, making the system more maintainable and testable.

