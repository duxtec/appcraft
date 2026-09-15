from typing import Any, TypeVar

from domain.models import Model, NewModel

TNewModel = TypeVar("TNewModel", bound=NewModel)

TModel = TypeVar("TModel", bound=Model[Any])
