import functools
from abc import ABC
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., object])


class Runner(ABC):
    @staticmethod
    def runner(
        func: Callable[..., object] | None = None, *, pause: bool = False
    ) -> Any:
        """Marks a method as a runner. `pause=True` waits for a keypress
        after the method finishes, so the output of a read-only command
        stays on screen. The `pause=true|false` argument overrides it."""

        def decorate(target: Callable[..., object]) -> Callable[..., object]:
            @functools.wraps(target)
            def wrapper(*args: list[Any], **kwargs: dict[Any, Any]):
                return target(*args, **kwargs)

            setattr(wrapper, 'is_app_runner', True)
            setattr(wrapper, 'pause_on_exit', pause)
            return wrapper

        if func is None:
            return decorate
        return decorate(func)

    @staticmethod
    def not_runner(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[Any, Any]):
            return func(*args, **kwargs)

        setattr(wrapper, 'is_app_runner', False)
        return cast(F, wrapper)
