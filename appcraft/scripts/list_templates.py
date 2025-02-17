from appcraft.template.base.files.infrastructure.framework.appcraft.utils.printer import Printer
from appcraft.utils.template_loader import TemplateLoader


def list_templates():
    tl = TemplateLoader()
    templates = tl.templates
    """
    templates = {
        "ci-cd": "Designed to facilitate Continuous Integration and Continuous Delivery (CI/CD). Includes configurations and scripts to automate testing and deployment.",
        "data-analysis": "A template geared towards data analysis projects. Includes libraries and structures for data manipulation, visualization, and reporting.",
        "database": "Provides a configuration for projects that interact with databases. Includes integrations with ORMs and data management scripts.",
        "flask": "A complete template for web applications based on Flask. Includes structures for route management, HTML templates, and integration with popular libraries.",
        "selenium": "Intended for web testing automation using Selenium. Includes examples and configurations to simplify writing and executing automated tests in browsers."
    }
    """
    Printer.title("Available Templates:", end="\n\n")
    for template in templates:
        if template.name == "base":
            continue

        Printer.success(template.name, end=": ")
        Printer.info(template.description)
        print()


if __name__ == "__main__":
    list_templates()
