from dataclasses import dataclass

from application.ports.remote_repository import RemoteRepositoryPort
from application.use_cases import UseCase


@dataclass(frozen=True)
class CreatePlatformReleaseInput:
    tag: str
    title: str
    notes: str
    prerelease: bool


class CreatePlatformReleaseUseCase(
    UseCase[CreatePlatformReleaseInput, str]
):
    def __init__(self, remote_repository: RemoteRepositoryPort) -> None:
        self.remote_repository = remote_repository

    def execute(self, input_data: CreatePlatformReleaseInput) -> str:
        return self.remote_repository.create_release(
            tag=input_data.tag,
            title=input_data.title,
            notes=input_data.notes,
            prerelease=input_data.prerelease,
        )
