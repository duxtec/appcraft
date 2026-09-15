from __future__ import annotations

from abc import ABC
from typing import (
    Annotated,
    Any,
    Iterable,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel, model_validator

from domain.models.core.field import Field
from domain.models.core.pk import PK
from domain.models.core.typing import resolve_annotation
from domain.value_objects.id import Id

IdType = TypeVar("IdType", bound=Id)


class PydanticSchema(BaseModel):
    model_config = {"frozen": True}


class PydanticNewModel(BaseModel, ABC):
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        # model_fields já está pronto neste ponto (o metaclass do Pydantic
        # roda antes de __init_subclass__), então é seguro anexar aqui.
        apply_typed_fields_pydantic(cls)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any):
        super().__pydantic_init_subclass__(**kwargs)
        apply_typed_fields_pydantic(cls)

    @classmethod
    def primary_keys(cls) -> list[Field[Any]]:
        hints = get_type_hints(cls, include_extras=True)

        return [
            getattr(cls, field)
            for field, hint in hints.items()
            if PK.is_pk(hint)
        ]

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="before")
    @classmethod
    def _coerce_value_objects(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        for name, _ in cls.model_fields.items():
            if name not in data:
                continue

            annotation = getattr(cls, name)._type

            data[name] = _coerce_value(data[name], annotation)

        return cast(Any, data)


PRIMITIVES = (int, str, float, bool)


def _unwrap_optional(tp: Any):
    if get_origin(tp) is Union:
        args = [a for a in get_args(tp) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return tp


def _coerce_scalar(value: Any, field_type: Any):
    """Coage um valor único, se aplicável."""
    if not isinstance(field_type, type):
        return value
    if isinstance(value, field_type):
        return value
    if issubclass(field_type, (BaseModel,) + PRIMITIVES):
        return value
    if isinstance(value, PRIMITIVES):
        try:
            return field_type(value)
        except TypeError:
            return value
    return value


def _coerce_value(value: Any, annotation: Any) -> Any:
    annotation = _unwrap_optional(annotation)
    origin = get_origin(annotation)

    if origin in (list, set, frozenset, tuple):
        args = get_args(annotation)
        if not args or value is None:
            return value
        item_type = args[0]
        if not isinstance(value, (list, set, frozenset, tuple)):
            return value

        items = cast(Iterable[Any], value)
        coerced_items = [_coerce_scalar(v, item_type) for v in items]

        if origin is list:
            return list(coerced_items)
        if origin is set:
            return set(coerced_items)
        if origin is frozenset:
            return frozenset(coerced_items)
        return tuple(coerced_items)  # origin is tuple

    if origin is dict:
        args = get_args(annotation)
        if len(args) != 2 or value is None or not isinstance(value, dict):
            return value
        _, value_type = args
        items_dict = cast(dict[Any, Any], value)
        return {
            k: _coerce_scalar(v, value_type) for k, v in items_dict.items()
        }

    return _coerce_scalar(value, annotation)


def apply_typed_fields_pydantic(cls: type[BaseModel]) -> None:
    type_hints = get_type_hints(
        cls,
        include_extras=True,
    )
    mapping = build_typevar_map(cls)

    for name in cls.model_fields:
        existing = cls.__dict__.get(name)
        if isinstance(existing, Field) and existing.owner is cls:
            continue
        hint = type_hints[name]

        type_ = resolve_annotation(hint, mapping)

        if get_origin(type_) is Annotated:
            type_, *_ = get_args(type_)

        if get_origin(type_) is Field:
            (type_,) = get_args(type_)

        descriptor: Field[Any] = Field(type_=type_)
        descriptor.__set_name__(cls, name)
        setattr(cls, name, descriptor)


def build_typevar_map(cls: type) -> dict[TypeVar, Any]:
    mapping: dict[TypeVar, Any] = {}

    for base in cls.__bases__:
        metadata = getattr(base, "__pydantic_generic_metadata__", None)
        if not metadata:
            continue

        origin = metadata.get("origin")
        args = metadata.get("args", ())

        if origin is None:
            continue

        parameters = getattr(origin, "__parameters__", ())

        mapping.update(zip(parameters, args))

    return mapping
