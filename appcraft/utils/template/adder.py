import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import toml

from appcraft.templates.template_manager import TemplateManager
from appcraft.utils import (
    PackageManager,
    PipenvManager,
    PoetryManager,
    Printer,
)
from appcraft.utils.exceptions import TemplateNotFoundError
from appcraft.utils.file.ignore import is_build_artifact


class TemplateAdder:
    def __init__(
        self,
        target_dir: Path | None = None,
        package_manager: PackageManager = PoetryManager(),
    ):
        self.target_dir = Path(target_dir) if target_dir else Path(os.getcwd())
        self.package_manager = package_manager

    def add_template(self, template_name: str):

        template_dir = Path(__file__).parents[2] / "templates" / template_name

        template_files_dir = template_dir / "files"

        if not os.path.exists(template_files_dir):
            raise TemplateNotFoundError(template_name)

        directory_contents = self._copy_directory_contents(
            template_files_dir, self.target_dir
        )

        project_template_folder = os.path.join(
            self.target_dir,
            "infrastructure",
            "framework",
            "appcraft",
            "templates",
            template_name,
        )

        if not os.path.exists(project_template_folder):
            os.makedirs(project_template_folder)

        template_data = {template_name: {"files": directory_contents}}

        TemplateManager(target_dir=self.target_dir).add_template(
            template_data
        )

    def union_dicts(self, dict1: dict[Any, Any], dict2: dict[Any, Any]):
        for prop, value in dict2.items():
            if prop in dict1:
                if isinstance(dict1[prop], dict) and isinstance(value, dict):
                    dict1[prop] = self.union_dicts(dict1[prop], dict2[prop])
                elif isinstance(dict1[prop], list) and isinstance(
                    value, list
                ):
                    value: Any = value
                    existing: set[Any] = set(dict1[prop])
                    dict1[prop].extend(
                        v
                        for v in value
                        if v not in existing and not existing.add(v)
                    )
            else:
                dict1[prop] = value
        return dict1

    def merge_toml(
        self, template_name: str, toml_name: str = "pyproject.toml"
    ):
        base_path = self.target_dir / toml_name
        template_dir = Path(__file__).parents[2] / "templates" / template_name
        file_in_template = template_dir / "files" / toml_name

        try:
            with open(base_path, 'r') as base_file:
                base_file = toml.load(base_file)

            with open(file_in_template, 'r') as custom_file:
                file_in_template = toml.load(custom_file)

            base_file = self.union_dicts(base_file, file_in_template)

            with open(base_path, 'w') as base_file_opened:
                toml.dump(base_file, base_file_opened)

        except FileNotFoundError:
            return
            # Printer.error(f"\
            # Error: {e}. Make sure the file dependence path is correct.")
        except subprocess.CalledProcessError as e:
            Printer.error(
                f"\
Error during the addition of dependencies for template '{template_name}': {e}"
            )

    def merge_pm_files(self, template_name: str):
        mapper: dict[type[PackageManager], str] = {
            PoetryManager: "pyproject.toml",
            PipenvManager: "Pipfile",
        }
        toml_name = mapper.get(
            self.package_manager.__class__, "pyproject.toml"
        )
        self.merge_toml(template_name=template_name, toml_name=toml_name)

    def _copy_directory_contents(
        self, src_dir: Path, dst_dir: Path
    ) -> list[Path]:
        directory_contents: list[Path] = []
        for item in os.listdir(src_dir):
            if is_build_artifact(item):
                continue

            s = src_dir / item
            d = dst_dir / item
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                files = self._copy_directory_contents(s, d)
                directory_contents.extend(files)
            else:
                if os.path.exists(d) and not self.can_overwrite(d):
                    continue

                if os.path.basename(s) in (
                    "Pipfile",
                    "Pipfile.lock",
                ) and not isinstance(self.package_manager, PipenvManager):
                    continue

                if os.path.dirname(s) in ("config") and isinstance(
                    self.package_manager, PoetryManager
                ):
                    continue

                shutil.copy2(s, d)
                relative_path = Path(
                    os.path.relpath(d, ".").replace("\\", "/")
                )
                directory_contents.append(relative_path)
        return directory_contents

    def can_overwrite(self, file_path: Path):
        # Does not allow overwriting any file.
        # Checks if the file already exists
        # Returns True if the file does not exist
        return not os.path.exists(file_path)
