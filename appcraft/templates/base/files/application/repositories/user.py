from typing import Sequence

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports.database import DatabasePort
from application.repositories import RepositoryBase
from domain.filters.interface import FilterInterface
from domain.models.user import NewUser, User
from domain.value_objects.id import Id


class UserRepository(RepositoryBase[User, NewUser]):
    model = User
    new_user = NewUser

    def __init__(self, adapter: DatabasePort) -> None:
        self.adapter = adapter

    def get(self, filters: Sequence[FilterInterface]):
        users = self.adapter.get(self.model, filters)
        return users

    def create(self, entity: NewUser):
        return self.adapter.create(self.model, entity)

    def update(self, entity: User) -> User:
        return self.adapter.update(self.model, entity)

    def update_by_id(
        self,
        id: Id | Keys,
        changes: Changes,
    ) -> User:
        return self.adapter.update_by_id(self.model, id, changes)

    def delete(self, entity: User) -> None:
        return self.adapter.delete(self.model, entity)
