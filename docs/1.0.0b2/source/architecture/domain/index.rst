Domain Layer
=============

The **Domain Layer** is the core of the application — its models, value objects, and the abstract contracts other layers implement. It has **no framework or infrastructure dependencies**: no ORM, no HTTP client, no CLI code. This is what makes it trivial to test and safe to reuse regardless of which database, web framework, or delivery mechanism a project ends up using.

What belongs here
------------------

- **Models** (``domain/models/``) — the business entities themselves.
- **Value Objects** (``domain/value_objects/``) — small, self-validating types for attributes with specific business meaning (an ``Id``, a ``Username``) instead of bare primitives.
- **Filters** (``domain/filters/``) — the vocabulary a repository query is expressed in (``EqualFilter``, ``LikeFilter``, ``InFilter``, ``MinFilter``, ``MaxFilter``), independent of any specific database.
- **Interfaces** (``<concept>/interface/``) — abstract contracts for domain-level concepts that have more than one concrete shape (see below).
- **Exceptions** specific to domain rules (e.g. ``domain/models/exceptions/``).

What to avoid here
-------------------

- **Business logic in other layers.** If a rule is about what makes a valid ``User`` or a valid ``App``, it belongs on the model itself (as a validator), not scattered across use cases.
- **Direct persistence.** The Domain Layer never talks to a database — that's what ``Port``/``Adapter`` (Application/Infrastructure) are for.
- **External dependencies.** No framework imports, no infrastructure imports. If a domain file needs to import something from ``infrastructure/`` or a third-party framework, that logic belongs in a different layer.
- **UI or presentation concerns.** The Domain Layer doesn't know or care how its data ends up on screen.

Naming convention: a pure contract, not ``I`` + name
------------------------------------------------------

A domain-level abstract contract never uses an ``I`` prefix (``HTMLElement``, not ``IHTMLElement``). It still lives in its own ``interface/`` subfolder next to the concept it belongs to — not in a shared ``domain/interfaces/`` grab-bag — regardless of whether its class name carries the word "Interface". For example, ``domain/html_elements/interface/__init__.py`` defines the contract hierarchy every HTML-handling engine (Selenium, Playwright, ...) implements:

.. code-block:: python

    # domain/html_elements/interface/__init__.py
    from abc import ABC, abstractmethod


    class HTMLElement(ABC):
        pass


    class HTMLReadingElement(HTMLElement, ABC):
        @property
        @abstractmethod
        def inner_html(self) -> str:
            pass

        @abstractmethod
        def has_attribute(self, name: str) -> bool:
            pass

The ``Interface`` suffix itself is reserved for when the plain name would actually be ambiguous — a sibling class competing for the same identity, or a name already well known for something else. Neither applies here: the chain (``HTMLElement`` → ``HTMLReadingElement`` → ``HTMLNavigationElement`` → ``HTMLInteractiveElement``) is already distinguished by its own words (``Reading``/``Navigation``/``Interactive``), not by a suffix, and nothing else wants the plain names. The same reasoning applies to ``Filter`` (``domain/filters/interface/__init__.py``) and ``ValueObject`` (``domain/value_objects/__init__.py``): each is a pure, zero-behavior contract, and each already has a ``*Base`` sibling with the shared concrete implementation (``FilterBase``, ``ValueObjectBase``) — the plain name goes to the contract, and ``Base`` marks the one with the real behavior.

Every domain-layer contract in the framework today falls into one of these two shapes, so none of them carries the ``Interface`` suffix any more. The suffix survives on exactly one class, and it's not even in ``domain/``: ``HTMLParserInterface`` (``infrastructure/web_scraping/parser/interface.py``) keeps it because ``html.parser.HTMLParser`` is a real, well-known standard-library class solving the same kind of problem — a bare ``HTMLParser`` here would be confused with it, which is worth a suffix to avoid.

Example: a domain model
------------------------

Models are Pydantic-backed (via the framework's own ``NewModel``/``Model`` base classes), not plain classes — this gives every model validation for free. ``domain/models/app.py``:

.. code-block:: python

    from typing import Literal

    from domain.models import NewModel
    from domain.models.core.pydantic import field_validator


    class App(NewModel):
        name: str
        version: str
        environment: Literal['development', 'production']
        debug_mode: bool

        @field_validator("name")
        @classmethod
        def validate_name(cls, value: str) -> str:
            if not value:
                raise ValueError("Name cannot be empty")
            return value

Notice the validator comes from ``domain.models.core.pydantic``, not ``pydantic`` directly — that's the *only* file in ``domain/`` allowed to import Pydantic itself, so a project that ever needs to drop Pydantic only has to rewrite that one file. When adding a validator to your own model, import ``field_validator`` (and anything else Pydantic-related) from there too, not from ``pydantic``.

A model that also has a database identity extends ``Model[IdType]`` instead, adding an ``id`` field — see ``domain/models/user.py``:

.. code-block:: python

    from domain.models import Model, NewModel
    from domain.models.core.field import Field
    from domain.value_objects.id import Id


    class UserId(Id):
        pass


    class NewUser(NewModel):
        username: Field[str]


    class User(NewUser, Model[UserId]):
        pass

Splitting ``NewUser`` (the data needed to create one) from ``User`` (a persisted one, with an ``id``) is a recurring pattern — it's what lets a ``Repository`` accept a ``NewUser`` for ``create()`` but return a full ``User`` back.

Example: a filter
-------------------

Concrete filters (``domain/filters/__init__.py``) are thin subclasses of a shared ``FilterBase``, parameterized by the value type they compare against:

.. code-block:: python

    from typing import Any, SupportsInt, TypeVar

    from domain.filters.base import FilterBase

    T = TypeVar("T", str, SupportsInt)


    class EqualFilter(FilterBase[T]):
        pass


    class LikeFilter(FilterBase[str]):
        pass


    class InFilter(FilterBase[list[Any]]):
        pass

A repository query is built by passing a list of these — e.g. ``[EqualFilter(User.id, some_id)]`` — instead of any database-specific query syntax; each ``Adapter`` (see the `Infrastructure Layer <../infrastructure/index.html>`_) is responsible for translating them into its own backend's query language.
