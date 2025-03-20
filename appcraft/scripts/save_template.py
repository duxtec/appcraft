import sys

from appcraft.utils import Printer
from appcraft.utils.template_saver import TemplateSaver


def save_template():
    if len(sys.argv) < 2:
        Printer.warning("Template name must be provider.")
        exit(1)

    template_name = sys.argv[1]
    TemplateSaver().save_template(template_name)
