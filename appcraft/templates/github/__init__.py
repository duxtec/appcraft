from ..template_abc import TemplateABC


class GitHubTemplate(TemplateABC):
    active = True
    description = "\
GitHub Template contributes a RemoteRepositoryPort adapter wrapping the \
`gh` CLI — creating/deleting repositories and platform releases on \
GitHub. It ships no runner of its own: the remote_repository template's \
generic create_repo/delete_repo runner works against this adapter once \
installed (see docs/agents/templates-git.md)."

    dependencies = ["remote_repository"]
