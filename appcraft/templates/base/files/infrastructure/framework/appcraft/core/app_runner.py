import functools
from abc import ABC


class AppRunnerInterface(ABC):
    @staticmethod
    def runner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(wrapper, 'is_app_runner', True)
        return wrapper

    @staticmethod
    def not_runner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(wrapper, 'is_app_runner', False)
        return wrapper
