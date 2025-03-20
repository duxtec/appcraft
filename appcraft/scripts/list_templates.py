from appcraft.utils import Printer
from appcraft.utils.template_loader import TemplateLoader


def list_templates():
    tl = TemplateLoader()
    templates = tl.templates

    Printer.title("Available Templates:", end="\n\n")
    for template in templates:
        if template.name == "base":
            continue

        Printer.success(template.name, end=": ", emoji=False)
        Printer.info(template.description, emoji=False)
        print()


if __name__ == "__main__":
    list_templates()
