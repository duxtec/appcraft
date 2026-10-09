from typing import Optional

from application.use_cases.remote_repository.create_repo import (
    CreateRepoInput,
    CreateRepoUseCase,
)
from application.use_cases.remote_repository.delete_repo import (
    DeleteRepoUseCase,
)
from domain.remote_repository.repo import RemoteRepo
from infrastructure.app.manager import AppManager
from infrastructure.utils.component_printer import (
    ComponentPrinter,
)
from infrastructure.core.runner.mode import (
    InvalidInputError,
    read_input,
)
from presentation.cli.validator.input import BasicTypeInput


class RemoteRepositoryCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "remote_repository"

        @classmethod
        def create_repo_successfully(cls, repo: RemoteRepo):
            cls.success(f"Repository '{repo.name}' successfully created!")

        @classmethod
        def create_repo_error(cls, name: str):
            cls.error(f"Error creating repository: {name}")

        @classmethod
        def delete_repo_successfully(cls, name: str):
            cls.success(f"Repository '{name}' successfully deleted!")

        @classmethod
        def delete_repo_error(cls, name: str):
            cls.error(f"Error deleting repository: {name}")

        @classmethod
        def delete_warning(cls, name: str):
            cls.warning(
                f"This permanently deletes the repository '{name}' on the "
                "platform, including its code, issues and releases. It "
                "can't be undone."
            )

        @classmethod
        def delete_aborted(cls):
            cls.info("Deletion aborted: the repository name didn't match.")

        @classmethod
        def no_platform_installed(cls):
            cls.error(
                "No remote hosting platform is installed (e.g. the "
                "github template)."
            )

    def __init__(
        self,
        create_repo_uc: CreateRepoUseCase,
        delete_repo_uc: DeleteRepoUseCase,
    ) -> None:
        self.create_repo_uc = create_repo_uc
        self.delete_repo_uc = delete_repo_uc

    def create_repo(
        self,
        name: str | None,
        description: str | None,
        is_private: Optional[str | bool],
    ) -> RemoteRepo | None:
        name = self._get_name(name)
        description = self._get_description(description)
        is_private = self._get_is_private(is_private)

        try:
            repo = self.create_repo_uc.execute(
                CreateRepoInput(
                    name=name,
                    description=description,
                    is_private=is_private,
                )
            )
            self.Printer.create_repo_successfully(repo)
            return repo
        except Exception:
            self.Printer.create_repo_error(name)
            return None

    def delete_repo(self, name: str | None, confirm_name: str | None = None):
        name = self._get_name(name)

        if confirm_name is None:
            self.Printer.delete_warning(name)
            typed = read_input(f"Type '{name}' to confirm: ", "confirm_name").strip()
            if typed != name:
                self.Printer.delete_aborted()
                return
        elif confirm_name != name:
            raise InvalidInputError(
                f"confirm_name '{confirm_name}' doesn't match the repository name '{name}'."
            )

        try:
            self.delete_repo_uc.execute(name)
            self.Printer.delete_repo_successfully(name)
        except Exception:
            self.Printer.delete_repo_error(name)

    def _get_name(self, name: str | None) -> str:
        if name is None:
            name = AppManager().name

        return BasicTypeInput[str].input(
            prompt="Enter the repository name: ",
            value=name,
            argument="name",
        )

    def _get_description(self, description: str | None) -> str:
        if description is None:
            description = AppManager().description

        return BasicTypeInput[str].input(
            prompt="Enter the repository description: ",
            value=description,
            argument="description",
        )

    def _get_is_private(self, is_private: Optional[str | bool]) -> bool:
        return BasicTypeInput[bool].input(
            prompt="Is the repository private (Y/N)?: ",
            value=is_private,
            argument="is_private",
        )
