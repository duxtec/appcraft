from dataclasses import dataclass

from application.ports.git import GitPort
from application.use_cases import UseCase


@dataclass(frozen=True)
class MergeBranchInput:
    source: str
    target: str


class MergeBranchUseCase(UseCase[MergeBranchInput, None]):
    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: MergeBranchInput) -> None:
        self.git.checkout(input_data.target)
        self.git.merge(input_data.source)
        self.git.push(input_data.target)
