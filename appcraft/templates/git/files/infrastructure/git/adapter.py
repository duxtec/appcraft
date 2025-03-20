import subprocess
from typing import List, Optional

from application.interfaces.adapters import AdapterInterface


class GitAdapter(AdapterInterface):

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = repo_path

    def run(self, command: List[str]):
        command = ["git"] + command

        subprocess.check_call(
            command,
            cwd=self.repo_path,
        )

    def init_local_repo(self):
        self.run(["init", "-b", "main"])
        self.run(["add", "."])
        self.run(["commit", "-m", "chore: initial commit"])

    @property
    def remote_repo(self):
        try:
            self.run(["remote", "get-url", "origin"])
        except subprocess.CalledProcessError:
            return None

    @remote_repo.setter
    def remote_repo(self, url: str | None):
        if url is None:
            self.run(["remote", "remove", "origin"])
            return
        if self.remote_repo:
            self.run(["remote", "set-url", "origin", url])
        else:
            self.run(["remote", "add", "origin", url])

        self.run(["push", "--all", "origin"])

    def create_branch(
        self, branch_name: str, source_branch_name: Optional[str] = None
    ):
        command = ["checkout", "-b", branch_name]
        if source_branch_name:
            command.append(source_branch_name)
        self.run(command)

    def push_branch(
        self,
        branch_name: str,
    ):
        self.run(["push", "origin", "-b", branch_name])
