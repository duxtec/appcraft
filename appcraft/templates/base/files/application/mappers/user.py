from application.mappers import MapperBase
from application.schemas.output.user import UserOutSchema
from domain.models.user import User


class UserMapper(MapperBase[User, UserOutSchema]):
    pass
