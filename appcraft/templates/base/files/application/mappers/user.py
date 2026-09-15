from application.mappers.bases import BaseMapper
from application.schemas.output.user import UserOutSchema
from domain.models.user import User


class UserMapper(BaseMapper[User, UserOutSchema]):
    pass
