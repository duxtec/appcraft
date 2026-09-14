import argparse
import os
import shutil
import sys

from infrastructure.framework.appcraft.core.package.manager.base import (
    PackageManagerBase,
)

from appcraft.utils import Printer
from appcraft.utils.template.loader import TemplateLoader


def project_init():
    tl = TemplateLoader(get_inactives=True)
    parser = argparse.ArgumentParser(
        description="Initialize the project with specified templates."
    )

    parser.add_argument(
        "templates",
        nargs="*",
        default=[],
        help="Names of the templates to add (default: base).",
    )
    parser.add_argument(
        "--install-inactive",
        action="store_true",
        help=(
            "Allow installing templates marked inactive (active=False), "
            "e.g. templates still under development."
        ),
    )

    args = parser.parse_args()

    requested_template_names: list[str] = args.templates
    template_names = tl.default_template_names + (
        requested_template_names or []
    )

    try:
        templates = tl.resolve(
            template_names,
            requested_template_names=requested_template_names,
            allow_inactive=args.install_inactive,
        )

        appcraft_root_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
        )

        template_dir = os.path.join(
            appcraft_root_path,
            "appcraft",
            'templates',
        )

        project_folder = os.getcwd()

        if (
            project_folder == appcraft_root_path
            or project_folder == os.path.join(template_dir, "temp", "files")
        ):
            temp_dir = os.path.join(template_dir, "temp", "files")
            if os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)

            os.makedirs(temp_dir, exist_ok=True)
            os.chdir(temp_dir)
            project_folder = temp_dir

        project_template_folder = os.path.join(
            project_folder,
            "infrastructure",
            "framework",
            "appcraft",
            "templates",
        )

        for template in templates:
            Printer.info(f"Installing the '{template.name}' template...")
            template.install(target_dir=project_folder)

        shutil.copy2(
            os.path.join(template_dir, "template_manager.py"),
            os.path.join(project_template_folder, "template_manager.py"),
        )

        shutil.copy2(
            os.path.join(template_dir, "template_abc.py"),
            os.path.join(project_template_folder, "template_abc.py"),
        )

        for template in tl.template_names:
            project_this_template_folder = os.path.join(
                project_template_folder, template
            )

            os.makedirs(project_this_template_folder, exist_ok=True)

            shutil.copy2(
                os.path.join(template_dir, template, "__init__.py"),
                os.path.join(project_this_template_folder, "__init__.py"),
            )

        Printer.info("Installing requirements...")

        package_manager = PackageManagerBase()
        package_manager.install_requirements()

        for template in templates:
            if template.post_install:
                Printer.info(f"\
Executing post install scripts from '{template.name}' template...")
                template.post_install(target_dir=project_folder)

        Printer.success("Project created!")
    except Exception as e:
        Printer.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    project_init()
