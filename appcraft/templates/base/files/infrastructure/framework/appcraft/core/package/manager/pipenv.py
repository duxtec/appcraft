import os
import subprocess
import sys

from infrastructure.framework.appcraft.core.package.manager import (
    PackageManager,
)
from infrastructure.framework.appcraft.core.printer import CorePrinter


class PipenvManager(PackageManager):
    def __init__(self):
        super().__init__()

        if not self.venv_is_active():
            self.check_and_install_package_manager()

    def check_and_install_package_manager(self):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "show", "pipenv"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            CorePrinter.package_manager_not_found("Pipenv")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pipenv"]
                )
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def venv_create(self):
        if self.venv_is_active():
            return

        try:
            subprocess.check_call(["pipenv", "install", "--ignore-pipfile"])
            CorePrinter.installation_success()
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def venv_activate(self):
        return

    def get_activate_command(self):
        return ""

    def install_requirements(
        self,
        requirements: str | None = None,
        include_dev_dependencies: bool = True,
    ):
        if self.venv_is_active():
            return
        try:
            if requirements and os.path.exists(requirements):
                command = ["pipenv", "install", "-r", requirements]
            else:
                # `pipenv install` alone only ever installs [packages] —
                # [dev-packages] needs --dev explicitly.
                command = ["pipenv", "install"]
                if include_dev_dependencies:
                    command.append("--dev")

            subprocess.check_call(command)
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name: str):
        if self.venv_is_active():
            command = ["pip", "install", package_name]
        else:
            command = ["pipenv", "install", package_name]

        if package_name not in self.attempted_packages:
            self.attempted_packages.add(package_name)
            try:
                subprocess.check_call(command)
                CorePrinter.installation_success()
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def run_command(self, command: list[str]):
        try:
            if not self.venv_is_active():
                command = ["pipenv", "run"] + command

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            sys.exit(1)
