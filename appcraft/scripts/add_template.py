import argparse
import sys

from infrastructure.framework.appcraft.core.package.manager.base import (
    PackageManagerBase,
)

from appcraft.utils import Printer
from appcraft.utils.template.loader import TemplateLoader


def add_template():
    tl = TemplateLoader(get_inactives=True)

    parser = argparse.ArgumentParser(
        description="Add templates to an existing project."
    )

    parser.add_argument(
        "templates",
        nargs="*",
        default=tl.default_template_names,
        help="Names of the templates to add (default: base).",
    )
    parser.add_argument(
        "--install-inactive",
        action="store_true",
        help=(
            "Allow adding templates marked inactive (active=False), "
            "e.g. templates still under development."
        ),
    )

    args = parser.parse_args()
    requested_template_names: list[str] = args.templates

    try:
        templates = tl.resolve(
            requested_template_names,
            allow_inactive=args.install_inactive,
        )

        for template in templates:
            Printer.info(f"Installing the '{template.name}' template...")
            template.install()

        Printer.info("Installing requirements...")
        PackageManagerBase().install_requirements()

        for template in templates:
            if template.post_install:
                Printer.info(f"\
Executing post install scripts from '{template.name}' template...")
                template.post_install()

        Printer.success("Templates added!")
    except Exception as e:
        Printer.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    add_template()
