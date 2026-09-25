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
    exclusive_group: str | None = None
    pre_install: Callable[..., None] | None = None
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
        from appcraft.utils.template.loader import TemplateLoader

        # A template in an exclusive_group (e.g. the package_manager
        # group shared by poetry/pipenv/uv) replaces whichever other
        # member of that group is currently installed, rather than
        # sitting alongside it — TemplateLoader.resolve() already
        # rejects requesting two members *together*, so reaching this
        # point with another member installed means a deliberate swap.
        if cls.exclusive_group is not None:
            installed = TemplateManager(target_dir=target_dir).load_templates()
            if installed:
                templates_by_name = {
                    t.name: t
                    for t in TemplateLoader(get_inactives=True).templates
                }
                for name in list(installed):
                    if name == cls.name:
                        continue
                    other = templates_by_name.get(name)
                    if (
                        other is not None
                        and other.exclusive_group == cls.exclusive_group
                    ):
                        other.uninstall(target_dir=target_dir)

        ta = TemplateAdder(
            target_dir=target_dir, package_manager=cls.package_manager
        )
        ta.add_template(cls.name)
        ta.merge_pm_files(cls.name)

    @classmethod
    def uninstall(cls, target_dir: Path | None = None) -> None:
        templates = TemplateManager(target_dir=target_dir).load_templates()

        owned_files = templates.get(cls.name, {}).get("files", [])
        files_owned_elsewhere = {
            file
            for name, data in templates.items()
            if name != cls.name
            for file in data.get("files", [])
        }

        base_dir = Path(target_dir) if target_dir else Path.cwd()
        for relative_path in owned_files:
            if relative_path in files_owned_elsewhere:
                continue
            file_path = base_dir / relative_path
            if file_path.is_file():
                file_path.unlink()

        TemplateManager(target_dir=target_dir).remove_template(cls.name)
