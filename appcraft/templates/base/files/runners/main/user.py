from typing import Optional

from application.repositories.user_repository import UserRepository
from application.services.user_service import UserService
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.memory.adapters.memory_adapter import MemoryAdapter
from presentation.cli.user import UserCLIPresentation


class UserRunner(AppRunnerInterface):
    def __init__(self) -> None:
        memory_adapter = MemoryAdapter()
        user_repository = UserRepository(memory_adapter)
        self.user_service = UserService(user_repository)
        self.presentation = UserCLIPresentation(self.user_service)

        # Simulating data population for testing/demonstration purposes
        self.user_service.create("John Doe")
        self.user_service.create("Mary Jane")
        self.user_service.create("Thiago Costa")

    @AppRunnerInterface.runner
    def list(self):
        self.presentation.list()

    @AppRunnerInterface.runner
    def create(self, username: Optional[str] = None):
        self.presentation.create(username)
        self.presentation.list()

    @AppRunnerInterface.runner
    def update(self, id: Optional[int] = None, username: Optional[str] = None):
        self.presentation.update(id, username)
        self.presentation.list()

    @AppRunnerInterface.runner
    def delete(self, id: Optional[int] = None):
        self.presentation.delete(id)
        self.presentation.list()
