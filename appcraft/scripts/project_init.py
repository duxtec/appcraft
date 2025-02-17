import sys
import argparse

from appcraft.template.base.files.infrastructure.\
    framework.appcraft.utils.printer import Printer

from appcraft.utils.template_loader import TemplateLoader

from appcraft.template.base.files.infrastructure.\
    framework.appcraft.core.package_manager\
    import PackageManager


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

        for template in templates:
            Printer.info(f"Installing the '{template.name}' template...")
            template.install()

        Printer.info("Installing requirements...")

        package_manager = PackageManager()
        package_manager.install_requirements()

        Printer.success("Project created!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    project_init()
