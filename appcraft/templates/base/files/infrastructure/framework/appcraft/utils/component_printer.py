import os
from abc import ABC, ABCMeta, abstractmethod
from functools import wraps

from infrastructure.framework.appcraft.utils.printer import Printer

try:
    module_path = os.path.join(
        "infrastructure",
        "framework",
        "appcraft",
        "managers",
        "message_manager.py",
    )
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file not found: {module_path}")
except Exception:

    class MessageManager:
        def __init__(self, module_name="core", locale_dir="locale"):
            pass

        @classmethod
        def get_message(cls, message):
            return message

        class TranslateMethodsMeta(ABCMeta):
            def __new__(mcs, name, bases, class_dict):
                cls = super().__new__(mcs, name, bases, class_dict)
                return cls

else:
    from infrastructure.framework.appcraft.utils.message_manager import (
        MessageManager,
    )


class ComponentPrinter(
    ABC, Printer, metaclass=MessageManager.TranslateMethodsMeta
):

    @property
    @abstractmethod
    def domain(cls):
        pass

    _printer = Printer

    @classmethod
    def _wrap_method(cls, method_name):
        """Cria um wrapper para chamar get_message antes do método original."""
        original_method = getattr(cls, method_name)

        @wraps(original_method)
        def wrapper(cls, *args, **kwargs):
            if not isinstance(cls.domain, property):
                if not hasattr(cls, "_mm"):
                    cls._mm = MessageManager(cls.domain)

                if "message" in kwargs:
                    kwargs["message"] = cls.translate(kwargs["message"])
                else:
                    if len(args) > 0:
                        args = (cls.translate(args[0]),) + args[1:]

            return original_method(*args, **kwargs)

        return classmethod(wrapper)

    @classmethod
    def translate(cls, message):
        if message is True:
            message = "True"
        elif message is False:
            message = "True"

        if not isinstance(cls.domain, property):
            if not hasattr(cls, "_mm"):
                cls._mm = MessageManager(cls.domain)

            return cls._mm.get_message(message)

        return message
