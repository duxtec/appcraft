import os
import subprocess
import sys
from abc import ABC, abstractmethod


class PackageManager(ABC):
    def __init__(self):
        self.attempted_packages: set[str] = set()
        self.requirements_installed = False

    @abstractmethod
    def check_and_install_package_manager(self):
        pass

    def _is_command_available(self, command: str) -> bool:
        """Whether `command --version` actually runs — true regardless
        of how it got installed (a standalone installer script, pipx,
        the OS package manager, or pip). Checking `pip show <command>`
        instead, as every concrete manager used to, only tells you
        whether it's registered as a package in *this* interpreter,
        which none of the standalone installers ever do."""
        try:
            subprocess.run(
                [command, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def _install_via_pip(self, pip_name: str, command: str) -> bool:
        """Best-effort fallback: `pip install <pip_name>`, only if pip
        itself is actually usable in this interpreter — never true for
        a venv `uv` itself created, which deliberately ships without
        pip. Returns whether `command` is runnable afterwards; never
        raises."""
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name]
            )
        except subprocess.CalledProcessError:
            return False

        return self._is_command_available(command)

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
    def install_requirements(
        self,
        requirements: str | None = None,
        include_dev_dependencies: bool = True,
    ):
        pass

    @abstractmethod
    def install_package(self, package_name: str):
        pass

    @abstractmethod
    def run_command(self, command: list[str]):
        pass


# Imported after PackageManager is defined above: .pip/.pipenv/.poetry/.uv
# each import PackageManager back from this same package — safe only
# because the class already exists in this module's namespace by the
# time those submodules execute.
from infrastructure.app.manager import AppManager  # noqa: E402

from .pip import PipManager  # noqa: E402
from .pipenv import PipenvManager  # noqa: E402
from .poetry import PoetryManager  # noqa: E402
from .uv import UvManager  # noqa: E402


def PackageManagerBase() -> PackageManager:
    default_pm = PoetryManager
    try:
        manager = AppManager().config.get("manager") or "poetry"
        pms = {
            "poetry": PoetryManager,
            "pipenv": PipenvManager,
            "pip": PipManager,
            "uv": UvManager,
        }
        return pms.get(manager, default_pm)()
    except Exception:
        return default_pm()
