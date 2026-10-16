Recipes
=======

These recipes add one feature from start to finish: a ``Product`` that can be created from the command line. Each recipe builds on the one before it, and the last one wires the pieces into a runner.

The code assumes a project created with ``appc init`` (the ``base`` template is always included). Without a database template, products are kept in memory for the length of one run. To keep them between runs, install a database template: see :doc:`../templates/sqlalchemy/index`.

Add a Model
-----------

A model is a domain entity. It lives in ``domain/models/`` and has no framework or storage code. Create ``domain/models/product.py``:

.. code-block:: python

    from domain.models import Model, NewModel
    from domain.models.core.field import Field
    from domain.value_objects.id import Id


    class ProductId(Id):
        pass


    class NewProduct(NewModel):
        name: Field[str]


    class Product(NewProduct, Model[ProductId]):
        pass

``NewProduct`` is the data before storage, with no id. ``Product`` adds the id that storage gives it. Follow the same shape as ``domain/models/user.py``.

Add the Schemas and Mapper
--------------------------

Schemas are the shapes that cross the boundary between presentation and the application layer. Input schemas describe what a caller sends; output schemas describe what comes back. Create ``application/schemas/input/product.py``:

.. code-block:: python

    from application.schemas import Schema


    class ProductInSchema(Schema):
        name: str

and ``application/schemas/output/product.py``:

.. code-block:: python

    from application.schemas import Schema


    class ProductOutSchema(Schema):
        id: int
        name: str

A mapper converts a domain model into its output schema. Create ``application/mappers/product.py``:

.. code-block:: python

    from application.mappers.bases import MapperBase
    from application.schemas.output.product import ProductOutSchema
    from domain.models.product import Product


    class ProductMapper(MapperBase[Product, ProductOutSchema]):
        pass

``MapperBase`` reads the model and schema from the subscript, so the class body stays empty.

Add a Repository
----------------

A repository is the application's view of one model. It talks to storage only through a port, so it does not need to know which database is installed. Create ``application/repositories/product.py``:

.. code-block:: python

    from application.ports.database import DatabasePort
    from application.repositories import RepositoryBase
    from domain.models.product import NewProduct, Product


    class ProductRepository(RepositoryBase[Product, NewProduct]):
        def __init__(self, adapter: DatabasePort) -> None:
            self.adapter = adapter

``RepositoryBase`` already forwards ``get``, ``create``, ``update``, ``update_by_id``, ``delete`` and ``delete_by_id`` to the adapter, so the class only needs the constructor. Write a method yourself only when it must differ from the default, such as a query that filters by something the adapter does not know. The model classes come from the subscript (``Product`` and ``NewProduct``), which is why the class body stays this short. ``UserRepository`` in ``application/repositories/user.py`` is a longer example that overrides five of the six methods.

Add a Use Case
--------------

A use case holds one business operation. It is the only place that decides what happens when a product is created. Create ``application/use_cases/product/create.py``:

.. code-block:: python

    from application.mappers.product import ProductMapper
    from application.repositories.product import ProductRepository
    from application.schemas.input.product import ProductInSchema
    from application.schemas.output.product import ProductOutSchema
    from application.use_cases import CreateUseCase
    from domain.models.product import NewProduct


    class CreateProductUseCase(CreateUseCase[ProductInSchema, ProductOutSchema]):
        def __init__(self, repository: ProductRepository) -> None:
            self.repository = repository

        def execute(self, input_data: ProductInSchema) -> ProductOutSchema:
            new_product = NewProduct(**input_data.model_dump())
            product = self.repository.create(new_product)
            return ProductMapper.to_schema(product)

The other operations follow the same pattern: ``ReadUseCase`` and ``ReadOneUseCase`` for reads, ``UpdateUseCase`` for changes and ``DeleteUseCase`` for removal, all in ``application/use_cases/__init__.py``. Name each file after its action, as ``user/create.py`` does.

Add a Presentation Class
------------------------

The presentation class is the only part that talks to the user. It asks for missing input, calls the use case and prints the result through a ``Printer``. Create ``presentation/cli/product.py``:

.. code-block:: python

    from application.schemas.input.product import ProductInSchema
    from application.schemas.output.product import ProductOutSchema
    from application.use_cases.product.create import CreateProductUseCase
    from infrastructure.core.runner.mode import read_input
    from infrastructure.utils.component_printer import (
        ComponentPrinter,
    )


    class ProductCLIPresentation:

        class Printer(ComponentPrinter):
            domain = "product"

            @classmethod
            def created(cls, product: ProductOutSchema):
                cls.success(f"Product '{product.id}' created successfully!")

        def __init__(self, create_uc: CreateProductUseCase) -> None:
            self.create_uc = create_uc

        def create(self, name: str | None) -> None:
            name = read_input("Product name: ", "name") if name is None else name
            product = self.create_uc.execute(ProductInSchema(name=name))
            self.Printer.created(product)

``read_input(prompt, argument)`` is the one function to use for every question a command asks. It prompts in interactive runs, and in ``interactive=false`` runs it raises an error that names ``argument`` instead. Calling ``input()`` directly skips that rule, so that question would ignore ``interactive=false``.

The ``Printer`` class holds every message the presentation prints. Add a classmethod for each message, rather than calling ``print()`` in the presentation body, so the wording stays in one place.

Add a Runner
------------

The runner is the entry point. It builds the objects the presentation needs and calls one of its methods. Create ``runners/tools/product.py``, because creating products is a maintenance task. Use ``runners/main/`` for commands that are part of the application's normal run:

.. code-block:: python

    from application.repositories.product import ProductRepository
    from application.use_cases.product.create import CreateProductUseCase
    from infrastructure.database.provider import get_default_database_adapter
    from infrastructure.core.runner import Runner
    from presentation.cli.product import ProductCLIPresentation


    class ProductRunner(Runner):
        def __init__(self) -> None:
            self.repository = ProductRepository(get_default_database_adapter())
            self.presentation = ProductCLIPresentation(
                create_uc=CreateProductUseCase(self.repository),
            )

        @Runner.runner
        def create(self, name: str | None = None):
            self.presentation.create(name)

Only methods marked with ``@Runner.runner`` appear as commands. Run the new command with arguments, or leave them out to be asked:

.. code-block:: bash

    python tools product ProductRunner create name=Keyboard

    python tools product ProductRunner create

    python tools product ProductRunner create interactive=false

The last command fails with ``Missing argument 'name'. Pass it as name=<value>.`` and exit status 1, which is what a script or CI job needs to see.

Store Products in a Database
----------------------------

The code above works without any template, because ``get_default_database_adapter()`` falls back to an in-memory adapter. To keep products after the run ends, install a database template and create the table for the new model. Both steps are covered on the SQLAlchemy page: :doc:`../templates/sqlalchemy/index`, section *Adding a table for a new model*.

Where to Go Next
----------------

- A new HTTP endpoint for the same use case: :doc:`../templates/flask_api/index`, section *Adding an API route*.
- A new web page for the same use case: :doc:`../templates/flask_ui/index`, section *Adding a page*.
- Reading the rules each layer follows: :doc:`../architecture/index`.
