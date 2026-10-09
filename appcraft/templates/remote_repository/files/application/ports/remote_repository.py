from abc import ABC, abstractmethod

from application.ports import Port
from domain.remote_repository.repo import RemoteRepo


class RemoteRepositoryPort(Port, ABC):
    @abstractmethod
    def is_available(self) -> bool:
        """Whether this platform's CLI is installed and authenticated."""
        pass

    @abstractmethod
    def create_repository(
        self, name: str, description: str, is_private: bool
    ) -> RemoteRepo:
        pass

    @abstractmethod
    def get_repository(self, name: str) -> RemoteRepo | None:
        pass

    @abstractmethod
    def delete_repository(self, name: str) -> None:
        pass

    @abstractmethod
    def get_default_branch(self) -> str | None:
        """The repository's default branch on the platform."""
        pass

    @abstractmethod
    def set_default_branch(self, name: str) -> None:
        pass

    @abstractmethod
    def create_release(
        self, tag: str, title: str, notes: str, prerelease: bool
    ) -> str:
        """Creates a platform release for an existing git tag, returning
        its URL."""
        pass
