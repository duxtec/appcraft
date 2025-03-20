from typing import Optional

from application.services.github import GitHubRepositoryService
from domain.github.models.repository import GitHubRepository
from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)
from presentation.cli.validator.input import BasicTypeInput


class GitHubCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "github"

        @classmethod
        def create_repo_successfully(cls, repo: GitHubRepository):
            cls.success(f"Repository '{repo.name}' successfully created!")

        @classmethod
        def create_repo_error(cls, name: str):
            cls.error(f"Error creating repository: {name}")

        @classmethod
        def delete_repo_successfully(cls, name: GitHubRepository):
            cls.success(f"Repository '{name}' successfully deleted!")

        @classmethod
        def delete_repo_error(cls, name: str):
            cls.error(f"Error deleting repository: {name}")

    def __init__(self, service: GitHubRepositoryService) -> None:
        self.service = service

    def create_repo(
        self,
        name: Optional[str],
        description: Optional[str],
        is_private: Optional[str | bool],
    ):
        name = self._get_name(name)
        description = self._get_description(description)
        is_private = self._get_is_private(is_private)

        try:
            repo = self.service.create(
                name=name, description=description, is_private=is_private
            )
            self.Printer.create_repo_successfully(repo)
        except Exception:
            self.Printer.create_repo_error(name)

    def delete_repo(
        self,
        name: Optional[str],
    ):
        name = self._get_name(name)

        try:
            self.service.delete(name=name)
            self.Printer.delete_repo_successfully(name)
        except Exception as e:
            print(e)
            self.Printer.delete_repo_error(name)

    def _get_name(self, name: Optional[str]) -> str:
        if name is None:
            name = AppManager().name

        return BasicTypeInput(str).input(
            prompt="Enter the repository name: ",
            value=name,
        )

    def _get_description(self, description: Optional[str]) -> str:
        if description is None:
            description = AppManager().description

        return BasicTypeInput(str).input(
            prompt="Enter the repository description: ",
            value=description,
        )

    def _get_is_private(self, is_private: Optional[str | bool]) -> bool:
        return BasicTypeInput(bool).input(
            prompt="Is the repository private (Y/N)?: ",
            value=is_private,
        )
