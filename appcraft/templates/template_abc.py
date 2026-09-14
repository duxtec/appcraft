from abc import ABC, ABCMeta
from pathlib import Path
from typing import Any, Callable, ClassVar

from infrastructure.framework.appcraft.core.package.manager import (
    PackageManager,
)
from infrastructure.framework.appcraft.core.package.manager.poetry import (
    PoetryManager,
)

from .template_manager import TemplateManager

# flake8: noqa: E501


class TemplateABCMeta(ABCMeta):
    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]):
        if bases:
            dct["name"] = dct["__module__"].split(".")[-1]

            if name != "TemplateABC" and (
                "description" not in dct or dct["description"] is None
            ):
                raise TypeError(f"{name} must define 'description'.")

            return super().__new__(cls, name, bases, dct)

    def __setattr__(cls, name: str, value: Any):
        if name in ["default", "description"]:
            raise AttributeError(f"\
Cannot modify class-level attribute '{name}'")
        super().__setattr__(name, value)


class TemplateABC(ABC, metaclass=TemplateABCMeta):
    name: str
    description: str
    package_manager: PackageManager = PoetryManager()
    default: bool = False
    active: bool = False
    standalone: bool = True
    post_install: Callable[..., None] | None = None
    dependencies: ClassVar[list[str]] = []

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(getattr(cls, "description", None), str):
            raise TypeError(f"{cls.__name__} must define 'description'.")
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def is_installed(cls) -> bool:
        if cls.name in TemplateManager().load_templates():
            return True
        return False

    @classmethod
    def install(cls, target_dir: Path | None = None) -> None:
        from appcraft.utils.template.adder import TemplateAdder

        ta = TemplateAdder(
            target_dir=target_dir, package_manager=cls.package_manager
        )
        ta.add_template(cls.name)
        ta.merge_pm_files(cls.name)

    @classmethod
    def uninstall(cls) -> None:
        pass
