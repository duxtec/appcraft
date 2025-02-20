from appcraft.templates.base.files.infrastructure.framework.\
    appcraft.utils.printer import (
        Printer,
    )
from appcraft.utils.template_loader import TemplateLoader


def list_templates():
    tl = TemplateLoader()
    templates = tl.templates

    Printer.title("Available Templates:", end="\n\n")
    for template in templates:
        if template.name == "base":
            continue

        Printer.success(template.name, end=": ")
        Printer.info(template.description)
        print()


if __name__ == "__main__":
    list_templates()
