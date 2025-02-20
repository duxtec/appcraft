from abc import ABC, ABCMeta, abstractmethod

from .template_manager import TemplateManager


class TemplateABCMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        if bases:
            dct["name"] = dct["__module__"].split(".")[-1]
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

    @property
    @abstractmethod
    def description(self):
        pass

    @classmethod
    def is_installed(cls) -> bool:
        if cls.name in TemplateManager.load_templates():
            return True
        return False

    @classmethod
    def install(cls) -> None:
        from appcraft.utils.template_adder import TemplateAdder

        ta = TemplateAdder()
        ta.add_template(cls.name)
        ta.merge_pipfiles(cls.name)

    @classmethod
    def uninstall(cls) -> None:
        pass
