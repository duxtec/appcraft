from typing import Any, TypeVar

from application.repositories import Repository

TRepository = TypeVar("TRepository", bound=Repository[Any, Any])
