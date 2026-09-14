import functools
from abc import ABC
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., object])


class Runner(ABC):
    @staticmethod
    def runner(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[Any, Any]):
            return func(*args, **kwargs)

        setattr(wrapper, 'is_app_runner', True)
        return cast(F, wrapper)

    @staticmethod
    def not_runner(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[Any, Any]):
            return func(*args, **kwargs)

        setattr(wrapper, 'is_app_runner', False)
        return cast(F, wrapper)
