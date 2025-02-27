import os
import subprocess
import sys
from typing import List, Optional

from infrastructure.framework.appcraft.core.core_printer import CorePrinter
from infrastructure.framework.appcraft.core.package_manager.interface import (
    PackageManagerInterface,
)


class PipManager(PackageManagerInterface):
    def check_and_install_package_manager(self):
        pass

    def venv_create(self):
        try:
            venv_path = os.path.join(os.getcwd(), ".venv")
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            CorePrinter.installation_success()
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def venv_activate(self):
        if self.venv_is_active():
            return

        activate_command = f"{self.get_activate_command()}"
        try:
            subprocess.check_call(activate_command, shell=True)
        except subprocess.CalledProcessError as e:
            CorePrinter.execution_error(str(e))
            sys.exit(1)

    def get_activate_command(self):
        venv_path = os.path.join(os.getcwd(), ".venv")
        if sys.platform == "win32":
            return f'"{os.path.join(venv_path, "Scripts", "activate.bat")}"'
        else:
            return f"source \"{os.path.join(venv_path, 'bin', 'activate')}\""

    def install_requirements(self, requirements: Optional[str] = None):
        try:
            if not requirements:
                requirements = "requirements.txt"
            self.run_command(["pip", "install" "-r", requirements])
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name: str):
        if package_name not in self.attempted_packages:
            self.attempted_packages.add(package_name)
            try:
                self.run_command(["pip", "install", package_name])
                CorePrinter.installation_success()
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def run_command(self, command: List[str]):
        try:
            activate_command = self.venv_activate()
            full_command = f"{activate_command} && {command}"

            subprocess.check_call(
                full_command, shell=True, executable="/bin/bash"
            )
        except subprocess.CalledProcessError:
            sys.exit(1)
