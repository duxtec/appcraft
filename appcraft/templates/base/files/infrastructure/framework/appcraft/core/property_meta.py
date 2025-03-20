from abc import ABCMeta
from typing import Any, TypeVar


class PropertyMeta(ABCMeta):
    _props = []

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwargs: dict[Any, Any],
    ) -> type:
        new_cls: type = super().__new__(cls, name, bases, namespace)
        cls._set_custom_class_getitem(new_cls)

        return new_cls

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwargs: dict[Any, Any],
    ):
        super().__init__(name, bases, namespace, **kwargs)
        cls._set_props(cls)

    @classmethod
    def _set_props(cls, concrete_class: type[Any]):
        props: list[str] = getattr(concrete_class, "_props", [])
        if props:
            params = cls._get_params(concrete_class)

            for i, param in enumerate(params):
                if len(props) > i:
                    setattr(concrete_class, props[i], param)

    @classmethod
    def _get_params(
        cls, namespace_or_cls: type[object] | object | dict[str, Any]
    ):
        params: tuple[Any, ...] = ()
        if not isinstance(namespace_or_cls, dict):
            concrete_class = namespace_or_cls
            if not isinstance(namespace_or_cls, type):
                concrete_class = namespace_or_cls.__class__

            namespace: dict[str, Any] = concrete_class.__dict__
        else:
            namespace = namespace_or_cls

        params = namespace.get("__parameters__", ())
        orig_bases = namespace.get("__orig_bases__", ())

        for orig_base in orig_bases:
            args: tuple[Any, ...] = getattr(orig_base, "__args__", ())
            params += args

        params = tuple(
            param for param in params if not isinstance(param, TypeVar)
        )

        return params

    @classmethod
    def _set_custom_class_getitem(cls, concrete_class: type[Any]):
        if not hasattr(concrete_class, "__class_getitem__"):

            def custom_class_getitem(cls: type[PropertyMeta], item: Any):
                parameters = getattr(cls, "__parameters__")
                setattr(cls, "__parameters__", parameters + (item,))
                cls._set_props(cls)
                return cls

            setattr(
                concrete_class,
                "__class_getitem__",
                classmethod(custom_class_getitem),
            )

        return concrete_class


class PropertySetter(metaclass=PropertyMeta):
    pass
