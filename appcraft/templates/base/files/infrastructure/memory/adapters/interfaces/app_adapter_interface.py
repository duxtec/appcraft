from abc import abstractmethod

from domain.models.app import App
from infrastructure.interfaces.adapter import AdapterInterface


class AppAdapterInterface(
    AdapterInterface,
):
    @abstractmethod
    def get(self) -> App:
        pass
