import os
import subprocess
import sys

from infrastructure.core.package.manager import (
    PackageManager,
)
from infrastructure.core.printer import CorePrinter


class UvManager(PackageManager):
    def __init__(self):
        super().__init__()

        if not self.venv_is_active():
            self.check_and_install_package_manager()

    def check_and_install_package_manager(self):
        if self._is_command_available("uv"):
            return

        CorePrinter.package_manager_not_found("uv")
        if self._install_via_pip("uv", "uv"):
            return

        CorePrinter.installation_error(
            "pip isn't available to install uv automatically. Install "
            "it yourself first: "
            "https://docs.astral.sh/uv/getting-started/installation/"
        )
        sys.exit(1)

    def venv_create(self):
        if self.venv_is_active():
            return

        try:
            # `uv sync` creates .venv and installs from pyproject.toml (and
            # uv.lock, generating it first if missing) in one step.
            subprocess.check_call(["uv", "sync"])
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
                subprocess.check_call(
                    ["uv", "pip", "install", "-r", requirements]
                )
            else:
                command = ["uv", "sync"]
                if not include_dev_dependencies:
                    command.append("--no-dev")
                subprocess.check_call(command)
            self.requirements_installed = True
        except subprocess.CalledProcessError as e:
            CorePrinter.installation_error(str(e))
            sys.exit(1)

    def install_package(self, package_name: str):
        if package_name not in self.attempted_packages:
            self.attempted_packages.add(package_name)
            try:
                subprocess.check_call(["uv", "add", package_name])
                CorePrinter.installation_success()
            except subprocess.CalledProcessError as e:
                CorePrinter.installation_error(str(e))
                sys.exit(1)

    def run_command(self, command: list[str]):
        try:
            command = ["uv", "run"] + command

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            sys.exit(1)
