from abc import abstractmethod

from domain.models.app import App


class AppAdapterInterface:
    @abstractmethod
    def get(self) -> App:
        pass
