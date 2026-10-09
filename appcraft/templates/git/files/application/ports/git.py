from abc import ABC, abstractmethod

from application.ports import Port


class GitPort(Port, ABC):
    @abstractmethod
    def init(self, branch: str) -> None:
        pass

    @abstractmethod
    def is_repository(self) -> bool:
        """Whether the project directory is already a git repository."""
        pass

    @abstractmethod
    def has_commits(self) -> bool:
        pass

    @abstractmethod
    def add_all(self) -> None:
        pass

    @abstractmethod
    def commit(self, message: str) -> None:
        pass

    @abstractmethod
    def has_changes(self) -> bool:
        """Whether the index has anything staged to commit."""
        pass

    @abstractmethod
    def current_branch(self) -> str:
        pass

    @abstractmethod
    def branch_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def create_branch(
        self, name: str, source: str | None = None
    ) -> None:
        pass

    @abstractmethod
    def checkout(self, name: str) -> None:
        pass

    @abstractmethod
    def list_branches(self) -> list[str]:
        pass

    @abstractmethod
    def merged_branches(self, into: str) -> list[str]:
        """Local branches whose commits are all reachable from `into`."""
        pass

    @abstractmethod
    def delete_branch(self, name: str) -> None:
        """Deletes a local branch, refusing one that isn't merged."""
        pass

    @abstractmethod
    def merged_remote_branches(self, into: str) -> list[str]:
        """Remote branches on `origin` merged into `into`, after fetching."""
        pass

    @abstractmethod
    def delete_remote_branch(self, name: str) -> None:
        pass

    @abstractmethod
    def merge(self, branch: str) -> None:
        """Merges `branch` into whichever branch is currently checked out."""
        pass

    @abstractmethod
    def push(self, branch: str | None = None) -> None:
        pass

    @abstractmethod
    def get_remote(self) -> str | None:
        pass

    @abstractmethod
    def set_remote(self, url: str | None) -> None:
        pass

    @abstractmethod
    def reachable_tags(self, ref: str = "HEAD") -> list[str]:
        """Every tag whose commit is an ancestor of (or is) `ref`."""
        pass

    @abstractmethod
    def unreleased_messages(self) -> list[str]:
        """Commit messages reachable from HEAD that no tag contains yet."""
        pass

    @abstractmethod
    def commits_since(self, ref: str | None) -> list[str]:
        """Full commit messages (subject + body) since `ref`, or every
        commit reachable from HEAD when `ref` is None."""
        pass

    @abstractmethod
    def commits_between(self, base: str, head: str) -> list[str]:
        """Full commit messages reachable from `head` but not `base`."""
        pass

    @abstractmethod
    def create_tag(self, name: str, message: str) -> None:
        pass

    @abstractmethod
    def push_tag(self, name: str) -> None:
        pass
