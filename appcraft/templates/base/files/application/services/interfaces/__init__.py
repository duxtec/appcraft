from abc import ABC, abstractmethod
from typing import Type

from application.interfaces.adapters import AdapterInterface
from domain.interfaces.repositories import RepositoryInterface


class ServiceInterface(ABC):
    @abstractmethod
    def __init__(self, *repository: Type[RepositoryInterface]) -> None:
        pass


class ServiceAdapterInterface(ABC):
    @abstractmethod
    def __init__(self, *adapter: Type[AdapterInterface]) -> None:
        pass
