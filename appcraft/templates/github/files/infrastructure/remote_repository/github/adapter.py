import json
import subprocess

from application.ports.remote_repository import RemoteRepositoryPort
from domain.exceptions.remote_repository import (
    PlatformCLINotAvailableError,
    PlatformNotAuthenticatedError,
    RepositoryNotFoundError,
)
from domain.remote_repository.repo import RemoteRepo


class GitHubAdapter(RemoteRepositoryPort):
    @classmethod
    def run(cls, command: list[str]) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                ["gh"] + command,
                text=True,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"gh {' '.join(command)} failed: {e.stderr.strip()}"
            ) from None

    def is_available(self) -> bool:
        try:
            self.run(["--version"])
        except FileNotFoundError:
            return False

        try:
            result = self.run(["auth", "status"])
        except RuntimeError:
            return False

        return "not logged in" not in result.stdout

    def _ensure_available(self) -> None:
        try:
            self.run(["--version"])
        except FileNotFoundError:
            raise PlatformCLINotAvailableError("gh") from None

        try:
            result = self.run(["auth", "status"])
        except RuntimeError:
            raise PlatformNotAuthenticatedError("gh") from None

        if "not logged in" in result.stdout:
            raise PlatformNotAuthenticatedError("gh")

    def create_repository(
        self, name: str, description: str, is_private: bool
    ) -> RemoteRepo:
        self._ensure_available()
        repo_name = name.replace(" ", "-")
        visibility = "--private" if is_private else "--public"

        self.run(
            [
                "repo",
                "create",
                repo_name,
                visibility,
                "--description",
                description,
                "--source=.",
                "--remote=origin",
            ]
        )

        return RemoteRepo(
            name=repo_name,
            url=self._repository_url(repo_name),
            description=description,
            is_private=is_private,
        )

    def _repository_url(self, name: str) -> str:
        try:
            result = self.run(
                ["repo", "view", name, "--json", "url", "--jq", ".url"]
            )
            return result.stdout.strip()
        except RuntimeError:
            raise RepositoryNotFoundError(name) from None

    def get_repository(self, name: str) -> RemoteRepo | None:
        repo_name = name.replace(" ", "-")
        try:
            result = self.run(
                [
                    "repo",
                    "view",
                    repo_name,
                    "--json",
                    "url,description,isPrivate",
                ]
            )
        except RuntimeError:
            return None

        data = json.loads(result.stdout)
        return RemoteRepo(
            name=repo_name,
            url=data["url"],
            description=data.get("description") or "",
            is_private=bool(data.get("isPrivate")),
        )

    def delete_repository(self, name: str) -> None:
        self._ensure_available()
        repo_name = name.replace(" ", "-")
        self.run(["repo", "delete", repo_name, "--yes"])

    def get_default_branch(self) -> str | None:
        self._ensure_available()
        result = self.run(
            ["repo", "view", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name"]
        )
        return result.stdout.strip() or None

    def set_default_branch(self, name: str) -> None:
        self._ensure_available()
        self.run(["repo", "edit", "--default-branch", name])

    def create_release(
        self, tag: str, title: str, notes: str, prerelease: bool
    ) -> str:
        self._ensure_available()
        command = [
            "release", "create", tag, "--title", title, "--notes", notes,
        ]
        if prerelease:
            command.append("--prerelease")

        self.run(command)
        result = self.run(
            ["release", "view", tag, "--json", "url", "--jq", ".url"]
        )
        return result.stdout.strip()


_github_adapter: GitHubAdapter | None = None


def get_github_adapter() -> GitHubAdapter:
    """Shared-singleton getter — the Provider and any code injecting
    GitHubAdapter directly get the same instance."""
    global _github_adapter
    if _github_adapter is None:
        _github_adapter = GitHubAdapter()
    return _github_adapter
