from domain.models.exceptions import ModelNotFoundError
from domain.models.user import User


class UserModelNotFoundError(ModelNotFoundError):
    def __init__(self) -> None:
        super().__init__(model=User)
