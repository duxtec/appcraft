from core.app import App
from services.database.user import User as UserService

class Users(App):
    
    @App.runner
    def lists(self):
        user_service = UserService()

        # Adiciona um usuário
        user_service.add_user("John Doe", "john@example.com")

        # Busca e exibe todos os usuários
        users = user_service.fetch_users()
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
