import filecmp
import os
import shutil
from pathlib import Path

from appcraft.templates.template_manager import TemplateManager
from appcraft.utils import Printer
from appcraft.utils.exceptions import TemplateNotFoundError
from appcraft.utils.file.ignore import is_ignored


class TemplateSaver:
    def __init__(
        self,
        target_dir: Path | None = None,
    ):
        appcraft_root_path = Path(__file__).resolve().parents[3]

        templates_folder = appcraft_root_path / "appcraft" / "templates"

        self.target_dir = target_dir or templates_folder

        self.temp_template_dir = Path(self.target_dir) / "temp"
        self.temp_template_files_dir = self.temp_template_dir / "files"

    def save_template(self, template_name: str):

        template_dir = self.target_dir / template_name

        template_files_dir = template_dir / "files"

        if not os.path.exists(template_files_dir):
            raise TemplateNotFoundError(template_name)

        other_templates_files: list[str] = []
        tm = TemplateManager(target_dir=self.temp_template_files_dir)
        installed_templates = tm.load_templates()

        for template, files in installed_templates.items():
            if template == template_name:
                continue

            other_templates_files.extend(files["files"])

        template_files = installed_templates[template_name]["files"]

        directory_contents = self._copy_directory_contents(
            src_dir=self.temp_template_files_dir,
            dst_dir=template_files_dir,
            do_not_copy=other_templates_files,
        )

        if directory_contents:
            Printer.success(f"Saved files in {template_name} template")
        else:
            Printer.warning(f"No files to save in {template_name} template")

        for content in directory_contents:
            content_str = str(content)
            if content_str not in installed_templates[template_name]["files"]:
                installed_templates[template_name]["files"].append(
                    content_str
                )
            Printer.info(content_str)
        print()

        removed_files = self._remove_old_files(
            template_files=template_files,
            src_dir=self.temp_template_files_dir,
            dst_dir=template_files_dir,
        )

        removed_folders: list[Path] = []

        if removed_files:
            Printer.warning(f"Removed files in {template_name} template")

        for path in removed_files:
            path_str = str(path)
            Printer.info(path_str)
            if path_str in installed_templates[template_name]["files"]:
                installed_templates[template_name]["files"].remove(path_str)
            removed_folders.extend(
                self._remove_old_directories(
                    removed_item=path, template_dir=template_files_dir
                )
            )
        print()

        if removed_folders:
            Printer.warning(f"Removed folders in {template_name} template")

        for path in removed_folders:
            Printer.info(str(path))

        tm.save_templates(installed_templates)

    def _copy_directory_contents(
        self, src_dir: Path, dst_dir: Path, do_not_copy: list[str]
    ) -> list[Path]:
        directory_contents: list[Path] = []
        for item in os.listdir(src_dir):
            s = src_dir / item
            d = dst_dir / item
            relative_path = Path(
                os.path.relpath(s, self.temp_template_files_dir).replace(
                    "\\", "/"
                )
            )

            if str(relative_path) in do_not_copy or is_ignored(relative_path):
                continue

            if os.path.isdir(s):
                if item == "__pycache__":
                    continue

                files = self._copy_directory_contents(s, d, do_not_copy)
                directory_contents.extend(files)
                continue

            os.makedirs(os.path.dirname(d), exist_ok=True)

            if not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False):
                shutil.copy2(s, d)
                directory_contents.append(relative_path)
        return directory_contents

    def _remove_old_files(
        self, template_files: list[Path], src_dir: Path, dst_dir: Path
    ) -> list[Path]:
        removed_files: list[Path] = []

        for item in template_files:
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)

            if not os.path.isfile(s):
                if os.path.isfile(d):
                    os.remove(d)
                    relative_path = Path(
                        os.path.relpath(
                            s, self.temp_template_files_dir
                        ).replace("\\", "/")
                    )
                    removed_files.append(relative_path)

        return removed_files

    def _remove_old_directories(self, removed_item: Path, template_dir: Path):
        removed_directories: list[Path] = []

        removed_file = os.path.join(template_dir, removed_item)
        folder = Path(removed_file).parent

        if not os.path.isdir(folder):
            return removed_directories

        ignore_folders = [
            "application",
            "docs",
            "domain",
            "infrastruture",
            "presentation",
            "runners/main",
            "runners/tools",
        ]

        if not os.listdir(folder):
            relative_path = Path(
                os.path.relpath(folder, template_dir).replace("\\", "/")
            )
            if relative_path not in ignore_folders:
                shutil.rmtree(folder)
                removed_directories.append(relative_path)
                removed_directories.extend(
                    self._remove_old_directories(
                        removed_item=folder, template_dir=template_dir
                    )
                )

        return removed_directories
