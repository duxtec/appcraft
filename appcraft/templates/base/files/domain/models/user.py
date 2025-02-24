from typing import Optional

from domain.models.interfaces import ModelInterface
from domain.value_objects.username import Username


class User(ModelInterface):

    def __init__(self, id: Optional[int], username: str):
        super().__init__(id)
        self.username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = Username(username).value

    def __repr__(self):
        return f"User(id={self._id}, username={self._username})"
