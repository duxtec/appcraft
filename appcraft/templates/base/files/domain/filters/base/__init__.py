from abc import ABC
from typing import Generic, Optional, TypeVar

from domain.filters.interface import FilterInterface
from domain.models.interfaces import ModelInterface

Value = TypeVar("Value")


class FilterBase(FilterInterface, Generic[Value], ABC):
    value: Value

    def __init__(
        self,
        model_property: property,
        value: Value,
        include: Optional[bool] = None,
        not_param: Optional[bool] = None,
    ):
        if not isinstance(model_property, property):
            raise TypeError(
                f"The model_property {model_property} must be a property."
            )

        if model_property.fget is None:
            raise ValueError("The model_property must have a getter method.")

        value_type = type[value]
        expected_type = self.__annotations__['value']
        model_property_type = type(model_property.fget(None))

        if value_type != expected_type or value_type != model_property_type:
            raise TypeError(
                f"\
Types mismatch: value_type={value_type}, \
expected_type={expected_type}, \
model_property_type={model_property_type}"
            )

        model_name = model_property.fget.__qualname__.split(".")[0]
        model = model_property.fget.__globals__[model_name]

        if not issubclass(model, ModelInterface):
            raise TypeError(
                f"\
The class of {model_property} must inherit from ModelInterface."
            )

        self.model = model
        self.property = model_property.fget.__name__
        self.value = value
        self.not_param = not_param
        self.include = include

    def __repr__(self):
        props_repr = []
        props_repr.append(f"model={self.model}")
        props_repr.append(f"property={self.property}")
        props_repr.append(f"value={self.value}")

        if self.not_param is not None:
            props_repr.append(f"not_param={self.not_param}")

        if self.include is not None:
            props_repr.append(f"include={self.include}")

        props_repr_str = ", ".join(props_repr)

        return f"<{self.__class__.__name__}({props_repr_str})>"
