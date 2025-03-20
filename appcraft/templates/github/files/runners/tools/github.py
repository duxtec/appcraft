from application.services.github import GitHubRepositoryService
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.github.adapter import GitHubAdapter
from presentation.cli.github import GitHubCLIPresentation


class GitHubRunner(AppRunnerInterface):
    def __init__(self) -> None:
        adapter = GitHubAdapter()
        self.service = GitHubRepositoryService(adapter=adapter)
        self.presentation = GitHubCLIPresentation(service=self.service)

    @AppRunnerInterface.runner
    def create_repo(
        self,
        name: str | None = None,
        description: str | None = None,
        is_private: str | None = None,
    ):
        self.presentation.create_repo(
            name=name, description=description, is_private=is_private
        )

    @AppRunnerInterface.runner
    def delete_repo(self, name: str | None = None):
        self.presentation.delete_repo(name=name)
