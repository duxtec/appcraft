from application.services.github import GitHubRepositoryService
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.github.adapter import GitHubAdapter
from presentation.cli.github import GitHubCLIPresentation


class GitHubRunner(Runner):
    def __init__(self) -> None:
        adapter = GitHubAdapter()
        self.service = GitHubRepositoryService(adapter=adapter)
        self.presentation = GitHubCLIPresentation(service=self.service)

    @Runner.runner
    def create_repo(
        self,
        name: str | None = None,
        description: str | None = None,
        is_private: str | None = None,
    ):
        self.presentation.create_repo(
            name=name, description=description, is_private=is_private
        )

    @Runner.runner
    def delete_repo(self, name: str | None = None):
        self.presentation.delete_repo(name=name)
