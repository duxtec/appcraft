from application.schemas import Schema


class UserOutSchema(Schema):
    id: int
    username: str
