from abc import ABC, abstractmethod
from typing import Generic, Type

from application.schemas import TSchema
from domain.types.model import TNewModel


class Mapper(ABC, Generic[TNewModel, TSchema]):
    model: Type[TNewModel]
    dto: Type[TSchema]

    @classmethod
    @abstractmethod
    def to_schema(cls, model: TNewModel) -> TSchema:
        pass

    @classmethod
    @abstractmethod
    def to_domain(cls, schema: TSchema) -> TNewModel:
        pass
