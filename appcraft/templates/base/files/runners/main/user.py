from application.providers.adapters.database import (
    get_default_database_adapter,
)
from application.repositories.user import UserRepository
from application.use_cases.user.create import CreateUserUseCase
from application.use_cases.user.delete import DeleteUserUseCase
from application.use_cases.user.get import ReadUserUseCase
from application.use_cases.user.update import UpdateUserUseCase
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.user import UserCLIPresentation


class UserRunner(Runner):
    def __init__(self) -> None:
        self.adapter = get_default_database_adapter()
        self.repository = UserRepository(self.adapter)
        self.create_uc = CreateUserUseCase(self.repository)
        self.read_uc = ReadUserUseCase(self.repository)
        self.update_uc = UpdateUserUseCase(self.repository)
        self.delete_uc = DeleteUserUseCase(self.repository)
        self.presentation = UserCLIPresentation(
            create_uc=self.create_uc,
            read_uc=self.read_uc,
            update_uc=self.update_uc,
            delete_uc=self.delete_uc,
        )

    @Runner.runner
    def list(self):
        self.presentation.list()

    @Runner.runner
    def create(self, username: str | None = None):
        self.presentation.create(username)

    @Runner.runner
    def update(self, id: int | None = None, username: str | None = None):
        self.presentation.update(id, username)

    @Runner.runner
    def delete(self, id: int | None = None):
        self.presentation.delete(id)
