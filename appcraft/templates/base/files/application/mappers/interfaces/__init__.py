from abc import ABC, abstractmethod

from application.dtos.interfaces import DTOInterface
from domain.models.interfaces import ModelInterface


class MapperInterface(ABC):
    @abstractmethod
    def to_dto(cls, model: ModelInterface) -> DTOInterface:
        pass

    @abstractmethod
    def to_domain(cls, dto: DTOInterface) -> ModelInterface:
        pass
