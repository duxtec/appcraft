from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.git.branching import (
    BranchingConfig,
    base_branch_name,
    initial_branches,
)


class InitRepositoryUseCase(UseCase[BranchingConfig, None]):
    """Sets up the configured branches. Works on a fresh project, and on a
    repository created some other way: the repository is only initialised
    when it doesn't exist, the first commit is only made when there are no
    commits, and branches that are already there are left alone."""

    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: BranchingConfig) -> None:
        base = base_branch_name(input_data)

        if not self.git.is_repository():
            self.git.init(base)
        if not self.git.has_commits():
            self.git.add_all()
            self.git.commit("chore: initial commit")

        if not self.git.branch_exists(base):
            self.git.create_branch(base)

        for branch in initial_branches(input_data):
            if not self.git.branch_exists(branch):
                self.git.create_branch(branch, source=base)
