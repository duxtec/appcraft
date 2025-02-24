from application.dtos.user_dto import UserDTO
from application.mappers.interfaces import MapperInterface
from domain.models.user import User


class UserMapper(MapperInterface):
    @staticmethod
    def to_dto(user: User):
        return UserDTO(id=user.id, username=user.username)

    @staticmethod
    def to_domain(user_dto: UserDTO):
        return User(
            id=user_dto.id,
            username=user_dto.username,
        )
