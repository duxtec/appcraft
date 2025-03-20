import subprocess
import sys
from typing import List

from application.interfaces.adapters import AdapterInterface
from domain.filters.interface import FilterInterface
from domain.github.models.repository import GitHubRepository
from infrastructure.git.adapter import GitAdapter


class GitHubAdapter(AdapterInterface):
    def __init__(self):
        if not self.is_installed():
            sys.stderr.write("Error: 'gh' (GitHub CLI) is not installed.\n")
            sys.exit(1)
        if not self.is_authenticated():
            sys.stderr.write(
                "Error: Not authenticated with GitHub CLI. Run 'gh auth login'.\n"
            )
            sys.exit(1)

    @classmethod
    def run_check_call(cls, command: List[str]):
        try:
            command = ["gh"] + command

            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            raise RuntimeError(
                F"Failed to execute command: {' '.join(command)}"
            ) from None

    @classmethod
    def run(cls, command: List[str]):
        try:
            command = ["gh"] + command

            return subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            raise RuntimeError(
                F"Failed to execute command: {' '.join(command)}"
            ) from None

    @classmethod
    def is_installed(cls) -> bool:
        try:
            cls.run(["--version"])
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def is_authenticated(cls) -> bool:
        try:
            result = cls.run(["auth", "status"])
            return "not logged in" not in result.stdout
        except subprocess.CalledProcessError:
            return False

    def create_repository(
        self, repo_name: str, is_private: bool = True
    ) -> GitHubRepository:
        repo_name = repo_name.replace(" ", "-")
        visibility = "--private" if is_private else "--public"
        self.run_check_call(
            [
                "repo",
                "create",
                repo_name,
                visibility,
                "--source=.",
                "--remote=origin",
            ]
        )
        return GitHubRepository(
            name=repo_name,
            url=self.get_repository_url(repo_name),
            description="",
            is_private=is_private,
        )

    def get_repository_url(self, repo_name: str) -> str:
        try:
            repo_name = repo_name.replace(" ", "-")
            result = self.run(
                ["repo", "view", repo_name, "--json", "url", "--jq", ".url"]
            )
            return result.stdout.strip()
        except RuntimeError:
            raise LookupError(f"Repository '{repo_name}' not found.")

    def get_repository(
        self,
        filters: List[FilterInterface] = [],
    ) -> List[GitHubRepository]:
        repo_name = filters[0].value.replace(" ", "-")
        try:
            url = self.get_repository_url(repo_name=repo_name)
            return [
                GitHubRepository(
                    name=repo_name, url=url, description="", is_private=True
                )
            ]
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Error retrieving repository URL: {e}\n")
            sys.exit(1)

    def delete_repository(self, repository: GitHubRepository) -> None:
        repo_name = repository.name.replace(" ", "-")
        self.run_check_call(
            [
                "repo",
                "delete",
                repo_name,
                "--yes",
            ]
        )
        GitAdapter().remote_repo = None
