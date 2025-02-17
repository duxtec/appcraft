from abc import ABC, abstractmethod
import inspect
import os

from appcraft.utils.template_adder import TemplateAdder


class TemplateABC(ABC):
    class AvailableStatus:
        active = "active"
        inactive = "inactive"

    @property
    def name(self) -> str:
        return self.class_name()

    @classmethod
    def class_name(cls) -> str:
        module_path = inspect.getfile(cls)
        return os.path.basename(os.path.dirname(module_path))

    _status: "AvailableStatus" = "active"
    _default: bool = False

    @property
    def status(self) -> "AvailableStatus":
        return self._status

    @status.setter
    def status(self, status: "AvailableStatus"):
        if status not in {
            self.AvailableStatus.active, self.AvailableStatus.inactive
        }:
            raise ValueError(
                f"\
Invalid status value. Expected 'active' or 'inactive', got '{status}'."
            )
        self._status = status

    @property
    def default(self) -> bool:
        return self._default

    @default.setter
    def default(self, default: bool):
        if isinstance(default, bool):
            raise ValueError(
                f"\
Invalid default value. Expected bool, got '{default}'."
            )
        self._default = default

    @property
    @abstractmethod
    def description(self):
        pass

    @classmethod
    @abstractmethod
    def is_installed(cls) -> bool:
        pass

    @classmethod
    def install(cls) -> None:
        ta = TemplateAdder()
        ta.add_template(cls.class_name())
        ta.merge_pipfiles(cls.class_name())

    @classmethod
    @abstractmethod
    def uninstall(cls) -> None:
        pass
