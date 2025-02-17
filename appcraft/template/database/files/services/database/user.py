from core.database import Database
from database.models.models import User as UserModel

class User:
    def __init__(self):
        self.db = Database()

    def add_user(self, name, email):
        db = self.db.get_session()
        new_user = UserModel(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return new_user

    def fetch_users(self):
        db = self.db.get_session()
        users = db.query(UserModel).all()
        db.close()
        return users
