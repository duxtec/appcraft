from application.dtos.interfaces import DTOInterface


class UserDTO(DTOInterface):
    def __init__(
        self,
        id: int,
        username: str,
    ):
        self.id = id
        self.username = username

    def to_dict(self):
        return {"id": self.id, "username": self.username}
