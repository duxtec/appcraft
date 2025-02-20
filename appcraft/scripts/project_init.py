import os
import shutil
import sys
import argparse

from appcraft.templates.base.files.infrastructure.\
    framework.appcraft.utils.printer import Printer

from appcraft.utils.template_loader import TemplateLoader

from appcraft.templates.base.files.infrastructure.\
    framework.appcraft.core.package_manager import PackageManager


def project_init():
    tl = TemplateLoader()
    parser = argparse.ArgumentParser(
        description="Initialize the project with specified templates."
    )

    parser.add_argument(
        "templates", nargs="*", default=[],
        help="Names of the templates to add (default: base)."
    )

    args = parser.parse_args()

    template_names = args.templates
    template_names = tl.default_template_names + (template_names or [])

    try:
        nonexistent_templates = [
            template for template in template_names
            if template not in tl.template_names
        ]

        if (nonexistent_templates):
            raise ValueError(
                f"\
The following templates do not exist: {', '.join(nonexistent_templates)}"
            )

        templates = [
            template for template in tl.templates
            if template.name in template_names
        ]

        template_dir = os.path.join(
            os.path.dirname(__file__), '..', 'templates',
        )

        project_template_folder = os.path.join(
            os.getcwd(), "infrastructure", "framework",
            "appcraft", "templates"
        )

        for template in templates:
            Printer.info(f"Installing the '{template.name}' template...")
            template.install()

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

            os.makedirs(
                project_this_template_folder,
                exist_ok=True
            )

            shutil.copy2(
                os.path.join(template_dir, template, "__init__.py"),
                os.path.join(
                    project_this_template_folder, "__init__.py"
                )
            )

        Printer.info("Installing requirements...")

        package_manager = PackageManager()
        package_manager.install_requirements()

        Printer.success("Project created!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    project_init()
