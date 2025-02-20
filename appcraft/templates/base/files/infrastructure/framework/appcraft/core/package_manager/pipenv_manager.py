import os
import subprocess
import sys

from infrastructure.framework.appcraft.core.core_printer import CorePrinter

from .package_manager_abc import PackageManagerABC


class PipenvManager(PackageManagerABC):
    def __init__(self):
        super().__init__()

        if not self.venv_is_active():
            self.check_and_install_pipenv()

    def check_and_install_pipenv(self):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "show", "pipenv"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            CorePrinter.pipenv_not_found()
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pipenv"]
                )
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def venv_create(self):
        if self.venv_is_active():
            return False

        try:
            subprocess.check_call(
                ["pipenv", "install", "--ignore-pipfile"]
            )
            CorePrinter.installation_success()
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def venv_activate(self):
        return

    def get_activate_command(self):
        return

    def install_requirements(self, requirements=None):
        if self.venv_is_active():
            return False

        try:
            if requirements and os.path.exists(requirements):
                subprocess.check_call(
                    ["pipenv", "install", "-r", requirements]
                )
            else:
                subprocess.check_call(["pipenv", "install"])
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name):
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

    def run_command(self, command):
        try:
            if not self.venv_is_active():
                command = ["pipenv", "run"] + command.split()

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            sys.exit(1)
