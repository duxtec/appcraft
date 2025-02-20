from ..template_abc import TemplateABC


class LogsTemplate(TemplateABC):
    active = True
    description = "\
Logs Template sets up logging configurations for the application. \
It provides log rotation, logging levels, and outputs for error tracking, \
ensuring that all application logs are captured and stored effectively."
