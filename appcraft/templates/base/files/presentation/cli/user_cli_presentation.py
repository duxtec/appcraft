from typing import List, Optional

from application.dtos.user_dto import UserDTO
from application.services.user_service import UserService
from domain.models.exceptions.user_model_not_found import (
    UserModelNotFoundError,
)
from domain.value_objects.id import Id
from domain.value_objects.username import Username
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)
from presentation.cli.validator.input_validator import InputCLIValidator


class UserCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "app"

        @classmethod
        def list(cls, users: List[UserDTO]):
            cls.title("List of users")
            for user in users:
                for prop, value in user.__dict__.items():
                    cls.info(prop, end=": ")
                    cls.print(value)
                print()

        @classmethod
        def list_ids(cls, users: List[UserDTO]):
            cls.title("List of user IDs")
            for i, user in enumerate(users):
                if i == len(users) - 1:
                    cls.info(user.id)
                else:
                    cls.info(user.id, end=", ")

        @classmethod
        def user_not_exist(cls, id: int):
            cls.error(f"User with id '{id}' not exist!")
            print()

        @classmethod
        def username_too_short(cls, username):
            cls.error(f"Username '{username}' too short")
            cls.error("Username must be at least 5 characters long.")
            print()

        @classmethod
        def create_successfully(cls, user: UserDTO):
            cls.success(f"User '{user.id}' created successfully!")
            print()

        @classmethod
        def update_successfully(cls, user: UserDTO):
            cls.success(f"User '{user.id}' updated successfully!")
            print()

        @classmethod
        def delete_successfully(cls, id: int):
            cls.success(f"User '{id}' deleted successfully!")
            print()

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def list(self) -> None:
        users = self.user_service.get()
        self.Printer.list(users)

    def list_ids(self) -> None:
        users = self.user_service.get()
        self.Printer.list_ids(users)

    def create(self, username: Optional[str] = None):
        username = self._get_username(username)
        user = self.user_service.create(username)
        self.Printer.create_successfully(user)

    def update(self, id: Optional[int] = None, username: Optional[str] = None):
        while True:
            try:
                id = self._get_id(id)
                username = self._get_username(username)
                user = self.user_service.update(id, username)
                self.Printer.update_successfully(user)
                return

            except UserModelNotFoundError:
                self.Printer.user_not_exist(id)
                id = None

    def delete(self, id: Optional[int] = None):
        while True:
            try:
                id = self._get_id(id)
                self.user_service.delete(id)
                self.Printer.delete_successfully(id)
                return
            except UserModelNotFoundError:
                self.Printer.user_not_exist(id)
                id = None

    def _get_id(self, id: Optional[int] = None):
        return InputCLIValidator().get_valid_input(
            prompt="Enter the ID: ",
            value_object=Id,
            value=id,
        )

    def _get_username(self, username: Optional[str]):
        return InputCLIValidator().get_valid_input(
            prompt="Enter the username: ",
            value_object=Username,
            value=username,
        )
