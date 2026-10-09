from application.ports.git import GitPort
from application.use_cases import UseCase
from application.use_cases.git.list_cleanup_branches import CleanupCandidates


class DeleteBranchesUseCase(UseCase[CleanupCandidates, None]):
    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: CleanupCandidates) -> None:
        for branch in input_data.local:
            self.git.delete_branch(branch)
        for branch in input_data.remote:
            self.git.delete_remote_branch(branch)
