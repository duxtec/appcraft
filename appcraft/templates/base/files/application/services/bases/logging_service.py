from abc import ABC, abstractmethod
from typing import Type

from domain.interfaces.repositories import RepositoryInterface


class BaseLoggingService(ABC):
    @abstractmethod
    def __init__(self, *repository: Type[RepositoryInterface]) -> None:
        pass
