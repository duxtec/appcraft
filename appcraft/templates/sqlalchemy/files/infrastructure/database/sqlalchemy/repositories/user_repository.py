from domain.models.user import User
from infrastructure.database.sqlalchemy.models.user_db import UserDB
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> None:
        user_db = UserDB(username=user.username)
        self.session.add(user_db)
        self.session.commit()

    def get_by_id(self, user_id: int) -> User:
        user_db = self.session.query(UserDB).filter_by(id=user_id).first()
        if user_db:
            return User(id=user_db.id, username=user_db.username)
        return None

    def get_all(self) -> list[User]:
        users_db = self.session.query(UserDB).all()
        return [
            User(id=user_db.id, username=user_db.username)
            for user_db in users_db
        ]
