from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.git.branching import (
    BranchingConfig,
    base_branch_name,
    entry_branch_name,
    next_major_config,
)


class CutMajorVersionUseCase(UseCase[BranchingConfig, BranchingConfig]):
    """Creates the next major-version line's entry branch (its least
    stable stage, e.g. v1-alpha) from the current line's base (most
    stable, e.g. v0-main) branch — a no-op if it already exists. Only the
    entry branch is created: the new major line is unproven and has to
    earn promotion through beta/main like anything else, it doesn't start
    with a "stable" branch already in place. Never touches the existing
    major line; it keeps receiving fixes independently."""

    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: BranchingConfig) -> BranchingConfig:
        old_base = base_branch_name(input_data)
        new_config = next_major_config(input_data)
        new_branch = entry_branch_name(new_config)

        if not self.git.branch_exists(new_branch):
            self.git.create_branch(new_branch, source=old_base)

        return new_config
