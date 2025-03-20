from abc import ABC
from typing import Type

from automapper import mapper  # type: ignore

from application.mappers.interfaces import MapperInterface
from domain.types.dto import DTOType
from domain.types.model import ModelType
from infrastructure.framework.appcraft.core.property_meta import PropertyMeta


class BaseMapper(
    MapperInterface[ModelType, DTOType],
    ABC,
    metaclass=PropertyMeta,
):
    model: Type[ModelType]
    dto: Type[DTOType]
    _props = ["model", "dto"]

    @classmethod
    def to_dto(cls, model: ModelType) -> DTOType:
        return mapper.to(cls.dto).map(model)

    @classmethod
    def to_domain(cls, dto: DTOType) -> ModelType:
        return mapper.to(cls.model).map(dto)
