from abc import ABC, abstractmethod
import os


class PackageManagerABC(ABC):
    def __init__(self):
        self.attempted_packages = set()
        self.requirements_installed = False

    @abstractmethod
    def venv_create(self):
        pass

    @abstractmethod
    def venv_activate(self):
        pass

    def venv_is_active(self):
        return "VIRTUAL_ENV" in os.environ

    @abstractmethod
    def get_activate_command(self):
        pass

    @abstractmethod
    def install_requirements(self, requirements=None):
        pass

    @abstractmethod
    def install_package(self, package_name):
        pass

    @abstractmethod
    def run_command(self, command):
        pass
