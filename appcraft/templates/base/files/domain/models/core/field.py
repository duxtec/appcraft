from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    cast,
    get_args,
    get_origin,
    overload,
)

if TYPE_CHECKING:
    from domain.models import Model
    from domain.models.core.pydantic import CoreSchema, GetCoreSchemaHandler

T = TypeVar("T")


class Field(Generic[T]):
    def __init__(
        self,
        *,
        type_: type[T] | Any | None = None,
        pk: bool = False,
        default: T | None = None,
    ) -> None:
        self.pk = pk
        self.default = default
        self._type = type_

    @property
    def type(self) -> type[T]:
        t = self._type

        if get_origin(t) is Field:
            return get_args(t)[0]

        return cast(type[T], t)

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.owner = owner

    @overload
    def __get__(self, instance: None, owner: type) -> "Field[T]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> T: ...

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self.name] = value

    def __repr__(self) -> str:
        return f"{self.owner.__name__}.{self.name}"

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: "GetCoreSchemaHandler",
    ) -> "CoreSchema":
        args = get_args(source_type)

        if not args:
            return handler(Any)

        inner_type = args[0]

        return handler(inner_type)

    def is_primary_key(self) -> bool:
        owner = cast("type[Model[Any]]", self.owner)
        return self in owner.primary_keys()
