import importlib
from abc import ABC, ABCMeta
from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar

from infrastructure.framework.appcraft.utils.printer import Printer

try:
    locale_template_module = importlib.import_module(
        'infrastructure.framework.appcraft.templates.locales'
    )
    LocalesTemplates: type[Any] = locale_template_module.LocalesTemplates

    if LocalesTemplates.is_installed():

        message_manager_module = importlib.import_module(
            'infrastructure.framework.appcraft.utils.message_manager'
        )

        MessageManagerClass: type[Any] = message_manager_module.MessageManager
        TranslateMethodsMeta: type[ABCMeta] = (
            MessageManagerClass.TranslateMethodsMeta
        )

        TypeTranslateMethodsMeta = TypeVar(
            "TypeTranslateMethodsMeta",
            bound="MessageManager.TranslateMethodsMeta",
        )
    else:
        raise ImportError("Locales Templates not installed")

except Exception:
    TypeTranslateMethodsMeta = TypeVar(
        "TypeTranslateMethodsMeta", bound="MessageManager.TranslateMethodsMeta"
    )

    class MessageManager:
        def __init__(
            self, module_name: str = "core", locale_dir: str = "locale"
        ):
            pass

        @classmethod
        def get_message(cls, message: str) -> str:
            return message

        class TranslateMethodsMeta(ABCMeta):
            def __new__(
                mcs: Type[TypeTranslateMethodsMeta],
                name: str,
                bases: tuple[type, ...],
                class_dict: Dict[str, Any],
            ) -> TypeTranslateMethodsMeta:
                cls = super().__new__(mcs, name, bases, class_dict)
                return cls

    TranslateMethodsMeta: type[ABCMeta] = MessageManager.TranslateMethodsMeta

ComponentPrinterType = TypeVar(
    "ComponentPrinterType", bound="ComponentPrinter"
)


class ComponentPrinter(Printer, ABC, metaclass=TranslateMethodsMeta):
    DOMAIN: str = "core"

    _printer = Printer

    @classmethod
    def _wrap_method(cls: Type[ComponentPrinterType], method_name: str) -> Any:
        original_method: Callable[..., Any] = getattr(cls, method_name)

        @wraps(original_method)
        def wrapper(
            cls: ComponentPrinterType, *args: Any, **kwargs: Any
        ) -> Callable[..., Any]:
            if not isinstance(cls.DOMAIN, property):
                if not hasattr(cls, "_mm"):
                    cls._mm = MessageManager(cls.DOMAIN)

                if "message" in kwargs:
                    kwargs["message"] = cls.translate(kwargs["message"])
                else:
                    if len(args) > 0:
                        args = (cls.translate(args[0]),) + args[1:]

            return original_method(cls, *args, **kwargs)

        return classmethod(wrapper)

    @classmethod
    def translate(cls, message: str | bool):
        if message is True:
            message = "True"
        elif message is False:
            message = "True"

        if not hasattr(cls, "_mm"):
            cls._mm = MessageManager(cls.DOMAIN)

        return cls._mm.get_message(message)
