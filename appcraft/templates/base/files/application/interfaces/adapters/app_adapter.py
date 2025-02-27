from abc import ABC, abstractmethod

from domain.models.app import App


class AppAdapterInterface(ABC):
    @abstractmethod
    def get(self) -> App:
        pass
