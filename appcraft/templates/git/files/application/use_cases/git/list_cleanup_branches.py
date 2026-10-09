from dataclasses import dataclass

from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.git.branching import is_work_branch


@dataclass(frozen=True)
class CleanupCandidates:
    local: list[str]
    remote: list[str]


class ListCleanupBranchesUseCase(UseCase[str, CleanupCandidates]):
    """Work branches (`<type>/<name>`) already merged into `stable_branch`,
    locally and on `origin`. `stable_branch` itself and the checked-out
    branch are never candidates."""

    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: str) -> CleanupCandidates:
        current = self.git.current_branch()
        local = [
            branch
            for branch in self.git.merged_branches(input_data)
            if branch not in (input_data, current) and is_work_branch(branch)
        ]
        remote = [
            branch
            for branch in self.git.merged_remote_branches(input_data)
            if branch != input_data and is_work_branch(branch)
        ]
        return CleanupCandidates(local=local, remote=remote)
