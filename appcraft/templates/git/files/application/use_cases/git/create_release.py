from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.git.version import SemVer


class CreateReleaseUseCase(UseCase[SemVer, str]):
    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: SemVer) -> str:
        tag = f"v{input_data}"
        self.git.create_tag(tag, message=f"Release {tag}")
        self.git.push_tag(tag)
        return tag
