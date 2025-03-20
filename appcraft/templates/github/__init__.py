from ..template_abc import TemplateABC


class GitHubTemplate(TemplateABC):
    active = True
    description = "\
GitHub Template sets up a Git repository for version control. It includes \
pre-configured files like `.gitignore` and a default repository structure, \
ensuring that the project is ready to be tracked and managed with Git."

    dependencies: list[str] = ["git"]
