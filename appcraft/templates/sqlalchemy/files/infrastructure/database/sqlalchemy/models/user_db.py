from infrastructure.database.sqlalchemy.models.base import Base
from sqlalchemy import Column, String


class UserDB(Base):
    __tablename__ = "users"

    username = Column(String, nullable=False)

    def __init__(self, username: str):
        self.username = username

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
