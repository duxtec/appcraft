.. _application_flow:

===================
Application Flow
===================

This page describes the request and response flow through the layers, tying together the `Domain <../domain/index.html>`_, `Application <../application/index.html>`_, `Infrastructure <../infrastructure/index.html>`_, `Presentation <../presentation/index.html>`_, and `Runner <../runner/index.html>`_ pages into one end-to-end picture.

Request Flow
============

1. **Runner (entrypoint)** → instantiates the concrete adapter, repository, use case, and presentation classes, then calls the presentation.
2. **Presentation** → receives input, builds filters/schemas as needed.
3. **Use Case (Application)** → calls a **Repository**, applying any orchestration logic.
4. **Repository (Application)** → sends the domain model or filters to a **Port**.
5. **Adapter (Infrastructure)** → the concrete implementation of that **Port** — interacts with the actual database/service and returns a domain model.

Response Flow
=============

1. **Adapter (Infrastructure)** → returns the domain model (or a list of them).
2. **Repository (Application)** → returns it to the **Use Case**, unchanged.
3. **Mapper (Application)** → converts the domain model to a **Schema**.
4. **Use Case (Application)** → returns the schema.
5. **Presentation** → formats it for output (CLI printing, an HTTP response, ...).

This keeps every layer decoupled from the ones it doesn't directly depend on: swapping a database engine only touches the **Adapter**, and changing how output is formatted only touches **Presentation** — the **Use Case** in between doesn't need to change for either.
