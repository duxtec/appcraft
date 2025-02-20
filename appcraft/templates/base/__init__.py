from ..template_abc import TemplateABC


class BaseTemplate(TemplateABC):
    default = True
    active = True
    description = "\
Base template providing essential files and configurations for a structured, \
scalable, and customizable project setup."
