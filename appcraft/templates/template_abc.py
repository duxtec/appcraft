from abc import ABC, ABCMeta
from typing import Optional

from .template_manager import TemplateManager


class TemplateABCMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        if bases:
            dct["name"] = dct["__module__"].split(".")[-1]

            if name != "TemplateABC" and (
                "description" not in dct or dct["description"] is None
            ):
                raise TypeError(f"{name} must define 'description'.")

            return super().__new__(cls, name, bases, dct)

    def __setattr__(cls, name, value):
        if name in ["default", "description"]:
            raise AttributeError(
                f"\
Cannot modify class-level attribute '{name}'"
            )
        super().__setattr__(name, value)


class TemplateABC(ABC, metaclass=TemplateABCMeta):
    name: str
    description: str
    default: bool = False
    active: bool = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'description') or cls.description is None:
            raise TypeError(f"{cls.__name__} must define 'description'.")
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def is_installed(cls) -> bool:
        if cls.name in TemplateManager().load_templates():
            return True
        return False

    @classmethod
    def install(cls, target_dir: Optional[str] = None) -> None:
        from appcraft.utils.template_adder import TemplateAdder

        ta = TemplateAdder(target_dir=target_dir)
        ta.add_template(cls.name)
        ta.merge_pipfiles(cls.name)

    @classmethod
    def uninstall(cls) -> None:
        pass
