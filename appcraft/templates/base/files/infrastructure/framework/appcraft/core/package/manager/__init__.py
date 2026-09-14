import os
from abc import ABC, abstractmethod


class PackageManager(ABC):
    def __init__(self):
        self.attempted_packages: set[str] = set()
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
    def install_requirements(self, requirements: str | None = None):
        pass

    @abstractmethod
    def install_package(self, package_name: str):
        pass

    @abstractmethod
    def run_command(self, command: list[str]):
        pass
