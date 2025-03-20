import os
import sys
from typing import Optional

from appcraft.utils import Printer


class TemplateCreator:
    def __init__(
        self,
        target_dir: Optional[str] = None,
    ):
        appcraft_root_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
        )
        templates_folder = os.path.join(
            appcraft_root_path, "appcraft", "templates"
        )
        self.target_dir = target_dir or templates_folder
        self.base_template_dir = os.path.join(self.target_dir, "base")
        self.base_template_files_dir = os.path.join(
            self.base_template_dir, "files"
        )

    def create_template(self, template_name: str):

        template_dir = os.path.join(self.target_dir, template_name)

        template_files_dir = os.path.join(template_dir, "files")

        os.makedirs(template_files_dir, exist_ok=True)

        do_not_copy: list[str] = []
        do_not_copy.extend(
            [
                "infrastructure/framework/appcraft",
                "Pipfile",
                "Pipfile.lock",
                "poetry.lock",
                "config",
            ]
        )

        self._copy_directory_contents(
            src_dir=self.base_template_files_dir,
            dst_dir=template_files_dir,
            do_not_copy=do_not_copy,
        )

        self._create_runners(template_name)
        self._create_pyproject(template_name)
        self._create_template_file(template_name)

        Printer.success(f"Created {template_name} template")

    def _copy_directory_contents(
        self, src_dir: str, dst_dir: str, do_not_copy: list[str]
    ) -> list[str]:
        directory_contents: list[str] = []
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)
            relative_path = os.path.relpath(
                s, self.base_template_files_dir
            ).replace("\\", "/")

            if relative_path in do_not_copy:
                continue

            if os.path.isdir(s):
                if item == "__pycache__":
                    continue

                os.makedirs(d, exist_ok=True)

                files = self._copy_directory_contents(s, d, do_not_copy)
                directory_contents.append(relative_path)
                directory_contents.extend(files)
                continue

        return directory_contents

    def _create_runners(self, template_name: str):
        template_name_pascal_case = "".join(
            word.capitalize() for word in template_name.split("_")
        )
        runner_target_dir = os.path.join(
            self.target_dir, template_name, "files", "runners"
        )

        runners = [
            os.path.join("main", f"{template_name}.py"),
            os.path.join("tools", f"{template_name}.py"),
        ]

        for runner in runners:
            template_runner = os.path.join(runner_target_dir, runner)
            if os.path.exists(template_runner):
                Printer.warning(
                    f"⚠️ Skipping existing file: {template_runner}"
                )
                continue

            template_runner_content = f"""\
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)


class {template_name_pascal_case}Runner(AppRunnerInterface):
    @AppRunnerInterface.runner
    def start(self):
        print("{template_name_pascal_case} Runner Started")\n

    def non_runner1(self):
        # This method does not show in the runner.
        pass

"""

            with open(template_runner, "w", encoding="utf-8") as f:
                f.write(template_runner_content)

    def _create_pyproject(self, template_name: str):
        template_pyproject = os.path.join(
            self.target_dir, template_name, "files", "pyproject.toml"
        )

        if os.path.exists(template_pyproject):
            Printer.warning(f"⚠️ Skipping existing file: {template_pyproject}")
            return

        template_pyproject_content = f"""\
[tool.appcraft.{template_name}]
# Configs to the appcraft template '{template_name}'
"""

        with open(template_pyproject, "w", encoding="utf-8") as f:
            f.write(template_pyproject_content)

    def _create_template_file(self, template_name: str):
        template_name_pascal_case = "".join(
            word.capitalize() for word in template_name.split("_")
        )
        template_file = os.path.join(
            self.target_dir, template_name, "__init__.py"
        )

        if os.path.exists(template_file):
            Printer.warning(f"⚠️ Skipping existing file: {template_file}")
            return

        template_file_content = f"""\
from ..template_abc import TemplateABC


class {template_name_pascal_case}Template(TemplateABC):
    description = "\
{template_name_pascal_case} template description."
"""

        with open(template_file, "w", encoding="utf-8") as f:
            f.write(template_file_content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        Printer.error("Template name must be provider.")
        exit(1)

    template_name = sys.argv[1]
    TemplateCreator().create_template(template_name)
