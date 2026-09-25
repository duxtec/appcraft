from typing import Type

from application.mappers import Mapper
from application.schemas import TSchema
from domain.core.property_meta import PropertyMeta
from domain.types.model import TNewModel


class BaseMapper(
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
