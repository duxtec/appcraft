from ..template_abc import TemplateABC


class GitHubTemplate(TemplateABC):
    # Temporarily inactive: still on the pre-Port/use_cases architecture
    # (application/services/, AdapterInterface) — see
    # docs/agents/templates-git.md. Re-activate once migrated.
    active = False
    description = "\
GitHub Template sets up a Git repository for version control. It includes \
pre-configured files like `.gitignore` and a default repository structure, \
ensuring that the project is ready to be tracked and managed with Git."

    dependencies = ["git"]
