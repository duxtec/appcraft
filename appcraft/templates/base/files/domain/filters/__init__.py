from abc import ABC
from typing import Union

from domain.models.interfaces import ModelInterface


class FilterInterface(ABC):
    def __init__(
        self,
        model_property: property,
        value,
        include=None,
        not_param=None,
    ):
        if not isinstance(model_property, property):
            raise TypeError(
                f"The model_property {model_property} must be a property."
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


class MinFilter(FilterInterface):
    def __init__(
        self,
        model_property: property,
        value: Union[str, int],
        include=True,
        not_param=False,
    ):
        super().__init__(
            model_property=model_property,
            value=value,
            include=include,
            not_param=not_param,
        )


class MaxFilter(FilterInterface):
    def __init__(
        self,
        model_property: property,
        value: Union[str, int],
        include=True,
        not_param=False,
    ):
        super().__init__(
            model_property=model_property,
            value=value,
            not_param=not_param,
            include=include,
        )


class EqualFilter(FilterInterface):
    def __init__(
        self,
        model_property: property,
        value: Union[str, int],
        not_param=False,
    ):
        super().__init__(
            model_property=model_property, value=value, not_param=not_param
        )


class InFilter(FilterInterface):
    def __init__(
        self,
        model_property: property,
        value: Union[str, int],
        not_param=False,
    ):
        super().__init__(
            model_property=model_property, value=value, not_param=not_param
        )


class LikeFilter(FilterInterface):
    def __init__(
        self,
        model_property: property,
        value: Union[str, int],
        not_param=False,
    ):
        super().__init__(
            model_property=model_property, value=value, not_param=not_param
        )
