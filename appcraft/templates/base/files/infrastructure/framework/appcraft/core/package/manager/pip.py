import os
import shlex
import subprocess
import sys

from infrastructure.framework.appcraft.core.package.manager import (
    PackageManager,
)
from infrastructure.framework.appcraft.core.printer import CorePrinter


class PipManager(PackageManager):
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

    def install_requirements(self, requirements: str | None = None):
        try:
            if not requirements:
                requirements = "requirements.txt"
            self.run_command(["pip", "install", "-r", requirements])
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

    def run_command(self, command: list[str]):
        try:
            activate_command = self.get_activate_command()
            full_command = f"{activate_command} && {shlex.join(command)}"

            subprocess.check_call(
                full_command, shell=True, executable="/bin/bash"
            )
        except subprocess.CalledProcessError:
            sys.exit(1)
