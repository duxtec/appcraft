import logging
from abc import ABC, abstractmethod


class LoggerInterface(logging.Logger, ABC):
    Level = None

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.Level is None:
            raise TypeError(f"{cls.__name__} must define a 'Level' Enum.")

    @abstractmethod
    def _setup_handlers(self):
        pass

    @abstractmethod
    def _disable_logging_methods(self):
        pass

    @abstractmethod
    def reset_current_log(self):
        pass
