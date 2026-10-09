from ..template_abc import TemplateABC


class RemoteRepositoryTemplate(TemplateABC):
    active = True
    standalone = False
    dependencies = ["git"]
    description = (
        "Remote Repository Template is the foundational setup for hosting "
        "a project on a remote Git platform — the RemoteRepositoryPort "
        "contract, the generic create_repo/delete_repo runner, and a "
        "Provider resolving which installed platform backs it by default "
        "(config/remote_repository.toml's default_platform). It ships no "
        "concrete platform adapter of its own: install the github template "
        "(depends on this one) to get an actual RemoteRepositoryPort "
        "implementation. Built so gitlab/bitbucket-style siblings can be "
        "added later without touching this template."
    )
