from application.use_cases.remote_repository.create_repo import (
    CreateRepoUseCase,
)
from application.use_cases.remote_repository.delete_repo import (
    DeleteRepoUseCase,
)
from infrastructure.core.runner import Runner
from infrastructure.git.adapter import GitAdapter
from infrastructure.remote_repository.provider import (
    get_default_remote_repository_adapter,
)
from presentation.cli.remote_repository import RemoteRepositoryCLIPresentation


class RemoteRepository(Runner):
    def __init__(self) -> None:
        self.git = GitAdapter()
        self.adapter = get_default_remote_repository_adapter()
        self.presentation = RemoteRepositoryCLIPresentation(
            create_repo_uc=CreateRepoUseCase(self.adapter),  # type: ignore
            delete_repo_uc=DeleteRepoUseCase(self.adapter),  # type: ignore
        )

    @Runner.runner
    def create_repo(
        self,
        name: str | None = None,
        description: str | None = None,
        is_private: str | None = None,
    ):
        if self.adapter is None:
            self.presentation.Printer.no_platform_installed()
            return

        repo = self.presentation.create_repo(
            name=name, description=description, is_private=is_private
        )
        if repo is not None:
            self.git.set_remote(repo.url)

    @Runner.runner
    def delete_repo(
        self,
        name: str | None = None,
        confirm_name: str | None = None,
    ):
        if self.adapter is None:
            self.presentation.Printer.no_platform_installed()
            return

        self.presentation.delete_repo(name=name, confirm_name=confirm_name)
