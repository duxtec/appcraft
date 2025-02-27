from abc import ABC, ABCMeta
from functools import wraps
from typing import Optional

from infrastructure.framework.appcraft.utils.printer import Printer

try:
    from infrastructure.framework.appcraft.templates.locales import (
        LocalesTemplates,
    )

    if LocalesTemplates.is_installed():
        from infrastructure.framework.appcraft.utils.message_manager import (
            MessageManager,
        )
    else:
        raise ImportError("Locales Templates not installed")

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


class ComponentPrinter(
    ABC, Printer, metaclass=MessageManager.TranslateMethodsMeta
):
    DOMAIN: Optional[str] = None

    _printer = Printer

    @classmethod
    def _wrap_method(cls, method_name):
        """Cria um wrapper para chamar get_message antes do método original."""
        original_method = getattr(cls, method_name)

        @wraps(original_method)
        def wrapper(cls, *args, **kwargs):
            if not isinstance(cls.DOMAIN, property):
                if not hasattr(cls, "_mm"):
                    cls._mm = MessageManager(cls.DOMAIN)

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

        if cls.DOMAIN is not None:
            if not hasattr(cls, "_mm"):
                cls._mm = MessageManager(cls.DOMAIN)

            return cls._mm.get_message(message)

        return message
