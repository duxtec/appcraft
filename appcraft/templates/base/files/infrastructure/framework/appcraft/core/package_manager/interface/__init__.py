import os
from abc import ABC, abstractmethod
from typing import List, Optional, Set


class PackageManagerInterface(ABC):
    def __init__(self):
        self.attempted_packages: Set[str] = set()
        self.requirements_installed = False

    @abstractmethod
    def check_and_install_package_manager(self):
        pass

    @abstractmethod
    def venv_create(self):
        pass

    @abstractmethod
    def venv_activate(self):
        pass

    def venv_is_active(self):
        return "VIRTUAL_ENV" in os.environ

    @abstractmethod
    def get_activate_command(self) -> str:
        pass

    @abstractmethod
    def install_requirements(self, requirements: Optional[str] = None):
        pass

    @abstractmethod
    def install_package(self, package_name: str):
        pass

    @abstractmethod
    def run_command(self, command: List[str]):
        pass
