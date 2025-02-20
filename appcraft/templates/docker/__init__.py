from ..template_abc import TemplateABC


class DockerTemplate(TemplateABC):
    description = "\
Docker Template provides resources for containerizing the application using \
Docker. It includes a pre-configured Dockerfile, ensuring that the \
application can be easily built and deployed in a containerized environment."
