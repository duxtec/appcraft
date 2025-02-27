from application.dtos.user_dto import UserDTO
from application.mappers.bases import BaseMapper
from domain.models.user import User


class UserMapper(BaseMapper[User, UserDTO]):
    pass
