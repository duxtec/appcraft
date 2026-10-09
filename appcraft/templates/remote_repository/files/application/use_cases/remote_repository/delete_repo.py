from application.ports.remote_repository import RemoteRepositoryPort
from application.use_cases import UseCase


class DeleteRepoUseCase(UseCase[str, None]):
    def __init__(self, remote_repository: RemoteRepositoryPort) -> None:
        self.remote_repository = remote_repository

    def execute(self, input_data: str) -> None:
        self.remote_repository.delete_repository(input_data)
