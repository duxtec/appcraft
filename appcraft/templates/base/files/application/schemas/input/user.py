from application.schemas import Schema


class UserInSchema(Schema):
    username: str


class UserUpdateSchema(Schema):
    id: int
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None


class UserDeleteSchema(Schema):
    id: int
