from ..template_abc import TemplateABC


class PoetryTemplate(TemplateABC):
    default = True
    active = True
    description = "\
Poetry template that provides a preconfigured pyproject.toml \
for dependency management."
