from abc import ABC, abstractmethod

from infrastructure.interfaces.adapter import AdapterInterface


class RepositoryInterface(ABC):
    @abstractmethod
    def __init__(self, adapter: AdapterInterface) -> None:
        super().__init__()
