from dataclasses import dataclass

from application.ports.remote_repository import RemoteRepositoryPort
from application.use_cases import UseCase
from domain.remote_repository.repo import RemoteRepo


@dataclass(frozen=True)
class CreateRepoInput:
    name: str
    description: str
    is_private: bool


class CreateRepoUseCase(UseCase[CreateRepoInput, RemoteRepo]):
    def __init__(self, remote_repository: RemoteRepositoryPort) -> None:
        self.remote_repository = remote_repository

    def execute(self, input_data: CreateRepoInput) -> RemoteRepo:
        return self.remote_repository.create_repository(
            name=input_data.name,
            description=input_data.description,
            is_private=input_data.is_private,
        )
