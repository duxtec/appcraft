from abc import ABC, abstractmethod
from typing import Generic, Type

from application.schemas import TSchema
from domain.core.property_meta import PropertyMeta
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


class MapperBase(
    Mapper[TNewModel, TSchema],
    metaclass=PropertyMeta,
):
    model: Type[TNewModel]
    schema: Type[TSchema]
    _props = ["model", "schema"]

    @classmethod
    def to_schema(cls, model: TNewModel) -> TSchema:
        return cls.schema.model_validate(model, from_attributes=True)

    @classmethod
    def to_domain(cls, schema: TSchema) -> TNewModel:
        return cls.model.model_validate(schema, from_attributes=True)
