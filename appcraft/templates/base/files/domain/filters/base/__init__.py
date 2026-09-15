from abc import ABC
from typing import Any, Generic, TypeVar

from domain.filters.interface import FilterInterface
from domain.models import NewModel
from domain.models.core.field import Field

Value = TypeVar("Value", covariant=True)


class FilterBase(FilterInterface, Generic[Value], ABC):
    value: Value

    def __init__(
        self,
        field: Field[Value],
        value: Value,
        include: bool | None = None,
        not_param: bool | None = None,
    ):
        if not isinstance(field, Field):  # type: ignore
            raise TypeError(f"The field {field} must be a field.")

        model = field.owner

        if not issubclass(model, NewModel):
            raise TypeError(f"\
The class of {field} must inherit from ModelInterface.")

        self.model = model
        self.property = field.name
        self.value = value
        self.not_param = not_param
        self.include = include

    def _verify_types(self):
        pass

    def __repr__(self):
        props_repr: list[Any] = []
        props_repr.append(f"model={self.model}")
        props_repr.append(f"property={self.property}")
        props_repr.append(f"value={self.value}")

        if self.not_param is not None:
            props_repr.append(f"not_param={self.not_param}")

        if self.include is not None:
            props_repr.append(f"include={self.include}")

        props_repr_str = ", ".join(props_repr)

        return f"<{self.__class__.__name__}({props_repr_str})>"
