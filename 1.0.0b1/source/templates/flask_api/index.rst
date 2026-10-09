Flask API Template
=============================

The **Flask API Template** adds a JSON API on top of the shared `Flask Template <../flask/index.html>`_ — it depends on ``flask`` and can be installed together with, or independently of, the `Flask UI Template <../flask_ui/index.html>`_.

It adds a versioned **presentation layer** for API endpoints under ``presentation/web/api/v1/`` (``routes/``, ``schemas/``, ``errors/``), which ``flask``'s own router auto-discovers and mounts under ``/api/v1`` — no manual registration needed. The ``errors/`` folder ships as scaffolding for you to fill in with project-specific error handling.

If the ``sqlalchemy`` template is also installed, the shared ``flask`` template initializes the database connection automatically; without it, the API runs without persistence.

This template doesn't ship any dependency of its own — its only requirement, the ``flask`` package itself, is declared by the shared ``flask`` template it depends on.

Adding an API Route
-------------------

Put one module per resource in ``presentation/web/api/v1/routes/``. The module exports a ``register()`` function that returns a ``Blueprint``. ``FlaskRouter`` finds it, registers the blueprint and mounts it under ``/api/v1``. A module-level ``Blueprint`` object is found the same way.

The route below exposes the ``Product`` use case from :doc:`../../developing/recipes` as ``POST /api/v1/products``. It goes in ``presentation/web/api/v1/routes/product.py``:

.. code-block:: python

    from flask import Blueprint, jsonify, request

    from application.repositories.product import ProductRepository
    from application.schemas.input.product import ProductInSchema
    from application.use_cases.product.create import CreateProductUseCase
    from infrastructure.database.provider import get_default_database_adapter


    def register() -> Blueprint:
        bp = Blueprint("product", __name__)

        @bp.route("/products", methods=["POST"])
        def create_product():  # type: ignore
            repository = ProductRepository(get_default_database_adapter())
            create_uc = CreateProductUseCase(repository)
            payload = ProductInSchema(**request.get_json())
            product = create_uc.execute(payload)
            return jsonify(product.model_dump()), 201

        return bp

Nothing else needs registering. To check the route without starting a server, use Flask's test client:

.. code-block:: python

    from infrastructure.framework.flask.app import FlaskApp

    client = FlaskApp().app.test_client()
    response = client.post("/api/v1/products", json={"name": "Cable"})
    print(response.status_code, response.get_json())  # 201 {'id': <number>, 'name': 'Cable'}

The route itself stays thin: it reads the request, calls a use case and returns JSON. Business rules belong in the use case, as described in :doc:`../../developing/index`. Existing routes such as ``routes/user.py`` get their use cases from ``ApplicationContainer`` instead, which is another way to build them.
