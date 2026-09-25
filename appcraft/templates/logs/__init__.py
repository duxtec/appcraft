from ..template_abc import TemplateABC


class LogsTemplate(TemplateABC):
    # Temporarily inactive: ships a Pipfile declaring real dependencies
    # (structlog, rich, ...) but no pyproject.toml equivalent —
    # TemplateAdder only copies a Pipfile for Pipenv-based projects, so
    # for the default (Poetry) a project this template's own imports
    # fail until the framework's runtime auto-install self-heals them,
    # unreliably. Re-activate once a pyproject.toml fragment is added.
    active = False
    description = "\
Logs Template sets up logging configurations for the application. \
It provides log rotation, logging levels, and outputs for error tracking, \
ensuring that all application logs are captured and stored effectively."
