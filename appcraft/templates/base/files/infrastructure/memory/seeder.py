from __future__ import annotations

from typing import TYPE_CHECKING

from application.repositories.user import UserRepository
from application.schemas.input.user import UserInSchema
from application.use_cases.user.create import CreateUserUseCase

if TYPE_CHECKING:
    from infrastructure.memory.adapter import MemoryAdapter


class MemoryAdapterSeeder:

    def __init__(self, adapter: MemoryAdapter):
        self.adapter = adapter

    def seed(self) -> None:
        self.__seed_users()

    def __seed_users(self):
        user_repository = UserRepository(adapter=self.adapter)
        create_uc = CreateUserUseCase(repository=user_repository)
        create_uc.execute(UserInSchema(username="John Doe"))
        create_uc.execute(UserInSchema(username="Mary Jane"))
        create_uc.execute(UserInSchema(username="Thiago Costa"))
