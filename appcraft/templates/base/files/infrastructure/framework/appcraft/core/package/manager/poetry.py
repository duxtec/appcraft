import os
import subprocess
import sys

from infrastructure.framework.appcraft.core.package.manager import (
    PackageManager,
)
from infrastructure.framework.appcraft.core.printer import CorePrinter


class PoetryManager(PackageManager):
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

    def install_requirements(
        self,
        requirements: str | None = None,
        include_dev_dependencies: bool = True,
    ):
        if self.venv_is_active():
            return
        try:
            # Keeps poetry.lock in sync whenever pyproject.toml was just
            # edited (e.g. a template merging in its own dependencies) —
            # `poetry install` refuses to run otherwise. By default this
            # only locks newly added/changed dependencies, it doesn't bump
            # ones already locked.
            subprocess.check_call(["poetry", "lock"])

            if requirements and os.path.exists(requirements):
                subprocess.check_call(["poetry", "add", "-r", requirements])
            else:
                command = ["poetry", "install"]
                if not include_dev_dependencies:
                    # Every group (dev, or any other) is excluded — only
                    # [tool.poetry.dependencies] gets installed. A
                    # production-only dependency (e.g. gunicorn) must be
                    # declared there, not under a named group.
                    command += ["--only", "main"]
                subprocess.check_call(command)
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name: str):
        if self.venv_is_active():
            command = ["poetry", "add", package_name]
        else:
            self.check_and_install_package_manager()
            command = ["poetry", "add", package_name]

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
            command = ["poetry", "run"] + command

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            sys.exit(1)
