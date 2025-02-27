import os
import subprocess
import sys
from typing import List, Optional

from infrastructure.framework.appcraft.core.core_printer import CorePrinter
from infrastructure.framework.appcraft.core.package_manager.interface import (
    PackageManagerInterface,
)


class PoetryManager(PackageManagerInterface):
    def __init__(self):
        super().__init__()

        if not self.venv_is_active():
            self.check_and_install_package_manager()

    def check_and_install_package_manager(self):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "show", "poetry"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            CorePrinter.package_manager_not_found("Poetry")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "poetry"]
                )
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def venv_create(self):
        if self.venv_is_active():
            return

        try:
            subprocess.check_call(["poetry", "install"])
            CorePrinter.installation_success()
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def venv_activate(self):
        return

    def get_activate_command(self):
        return ""

    def install_requirements(self, requirements: Optional[str] = None):
        if self.venv_is_active():
            return

        try:
            if requirements and os.path.exists(requirements):
                subprocess.check_call(["poetry", "add", "-r", requirements])
            else:
                subprocess.check_call(["poetry", "install"])
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name: str):
        if self.venv_is_active():
            command = ["pip", "install", package_name]
        else:
            command = ["poetry", "add", package_name]

        if package_name not in self.attempted_packages:
            self.attempted_packages.add(package_name)
            try:
                subprocess.check_call(command)
                CorePrinter.installation_success()
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def run_command(self, command: List[str]):
        try:
            if not self.venv_is_active():
                command = ["poetry", "run"] + command

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            sys.exit(1)
