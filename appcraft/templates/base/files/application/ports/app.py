from abc import ABC, abstractmethod

from application.ports import Port
from domain.models.app import App


class AppPort(Port, ABC):
    @abstractmethod
    def get(self) -> App:
        pass
