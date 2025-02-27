from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from application.dtos.interfaces import DTOInterface
from domain.models.interfaces import ModelInterface

Model = TypeVar('Model', bound=ModelInterface)
DTO = TypeVar('DTO', bound=DTOInterface)


class MapperInterface(ABC, Generic[Model, DTO]):
    model: Type[Model]
    dto: Type[DTO]

    @classmethod
    @abstractmethod
    def to_dto(cls, model: Model) -> DTO:
        pass

    @classmethod
    @abstractmethod
    def to_domain(cls, dto: DTO) -> Model:
        pass
