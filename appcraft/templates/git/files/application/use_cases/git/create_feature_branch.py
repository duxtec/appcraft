from dataclasses import dataclass

from application.ports.git import GitPort
from application.use_cases import UseCase


@dataclass(frozen=True)
class CreateFeatureBranchInput:
    kind: str
    name: str
    base_branch: str


class CreateFeatureBranchUseCase(
    UseCase[CreateFeatureBranchInput, str]
):
    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: CreateFeatureBranchInput) -> str:
        branch = f"{input_data.kind}/{input_data.name}"
        self.git.create_branch(branch, source=input_data.base_branch)
        return branch
