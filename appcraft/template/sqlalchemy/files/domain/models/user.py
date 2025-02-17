class User:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username

    def __repr__(self):
        return f"User(id={self.user_id}, username={self.username})"
