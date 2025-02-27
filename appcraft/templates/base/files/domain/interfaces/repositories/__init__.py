from abc import ABC, abstractmethod

from application.interfaces.adapters import AdapterInterface


class RepositoryInterface(ABC):
    @abstractmethod
    def __init__(self, adapter: AdapterInterface) -> None:
        pass
