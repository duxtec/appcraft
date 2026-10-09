import os
import subprocess

from application.ports.git import GitPort
from domain.exceptions.git import GitError


class GitAdapter(GitPort):
    def __init__(self, repo_path: str | None = None) -> None:
        self.repo_path = repo_path

    def run(self, command: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                check=True,
                text=True,
                capture_output=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise GitError(
                f"git {' '.join(command)} failed: {e.stderr.strip()}"
            ) from None

    def init(self, branch: str) -> None:
        self.run(["init", "-b", branch])

    def is_repository(self) -> bool:
        return os.path.isdir(".git")

    def has_commits(self) -> bool:
        try:
            self.run(["rev-parse", "--verify", "-q", "HEAD"])
        except GitError:
            return False
        return True

    def add_all(self) -> None:
        self.run(["add", "."])

    def has_changes(self) -> bool:
        return bool(self.run(["status", "--porcelain"]).strip())

    def commit(self, message: str) -> None:
        self.run(["commit", "-m", message])

    def current_branch(self) -> str:
        return self.run(["branch", "--show-current"]).strip()

    def branch_exists(self, name: str) -> bool:
        try:
            self.run(["show-ref", "--verify", f"refs/heads/{name}"])
            return True
        except GitError:
            return False

    def create_branch(self, name: str, source: str | None = None) -> None:
        command = ["branch", name]
        if source:
            command.append(source)
        self.run(command)

    def checkout(self, name: str) -> None:
        self.run(["checkout", name])

    def list_branches(self) -> list[str]:
        output = self.run(["branch", "--format=%(refname:short)"])
        return [line.strip() for line in output.splitlines() if line.strip()]

    def merged_branches(self, into: str) -> list[str]:
        output = self.run(
            ["branch", "--merged", into, "--format=%(refname:short)"]
        )
        return [line.strip() for line in output.splitlines() if line.strip()]

    def delete_branch(self, name: str) -> None:
        self.run(["branch", "-d", name])

    def merged_remote_branches(self, into: str) -> list[str]:
        if self.get_remote() is None:
            return []
        self.run(["fetch", "--prune", "origin"])
        output = self.run(
            ["branch", "-r", "--merged", into, "--format=%(refname:short)"]
        )
        prefix = "origin/"
        return [
            line.strip()[len(prefix):]
            for line in output.splitlines()
            if line.strip().startswith(prefix)
            and "HEAD" not in line
        ]

    def delete_remote_branch(self, name: str) -> None:
        self.run(["push", "origin", "--delete", name])

    def merge(self, branch: str) -> None:
        # --no-verify: the commit-msg hook's job is to stop a *raw*
        # `git merge`/`git commit` from landing a breaking change on a
        # major-version branch. MergeBranchUseCase's caller (the `git
        # merge` runner command) already enforces the same policy itself
        # before calling this — redirecting to the next major-version
        # branch when needed — so re-running the hook here would just
        # block our own, already-validated merge.
        self.run(["merge", "--no-ff", "--no-verify", branch])

    def push(self, branch: str | None = None) -> None:
        if self.get_remote() is None:
            # No remote configured yet (e.g. right after `git init`, before
            # a repository was created on any hosting platform) — merging
            # or releasing locally is still useful on its own, so pushing
            # is best-effort, not a hard requirement.
            return

        if branch:
            self.run(["push", "origin", branch])
        else:
            self.run(["push"])

    def get_remote(self) -> str | None:
        try:
            return self.run(["remote", "get-url", "origin"]).strip()
        except GitError:
            return None

    def set_remote(self, url: str | None) -> None:
        if url is None:
            self.run(["remote", "remove", "origin"])
            return

        if self.get_remote():
            self.run(["remote", "set-url", "origin", url])
        else:
            self.run(["remote", "add", "origin", url])

        self.run(["push", "--all", "origin"])
        self.run(["push", "--tags", "origin"])

    def reachable_tags(self, ref: str = "HEAD") -> list[str]:
        output = self.run(["tag", "--merged", ref])
        return [tag.strip() for tag in output.splitlines() if tag.strip()]

    def commits_since(self, ref: str | None) -> list[str]:
        range_spec = f"{ref}..HEAD" if ref else "HEAD"
        return self._log_messages(range_spec)

    def unreleased_messages(self) -> list[str]:
        output = self.run(["log", "HEAD", "--not", "--tags", "--pretty=format:%B%x1e"])
        return [
            commit.strip()
            for commit in output.split("\x1e")
            if commit.strip()
        ]

    def commits_between(self, base: str, head: str) -> list[str]:
        return self._log_messages(f"{base}..{head}")

    def _log_messages(self, range_spec: str) -> list[str]:
        output = self.run(["log", range_spec, "--pretty=format:%B%x1e"])
        return [
            commit.strip()
            for commit in output.split("\x1e")
            if commit.strip()
        ]

    def create_tag(self, name: str, message: str) -> None:
        self.run(["tag", "-a", name, "-m", message])

    def push_tag(self, name: str) -> None:
        if self.get_remote() is None:
            return
        self.run(["push", "origin", name])
