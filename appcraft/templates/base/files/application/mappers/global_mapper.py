from application.dtos.interfaces import DTOInterface
from automapper import mapper
from domain.models.interfaces import ModelInterface


class GlobalMapper:

    def __init__(self, model: type[ModelInterface], dto: type[DTOInterface]):
        self.model = model
        self.dto = dto

    def to_dto(self, model: ModelInterface) -> DTOInterface:
        return mapper.to(self.dto).map(model)

    def to_domain(self, dto: DTOInterface) -> ModelInterface:
        return mapper.to(self.model).map(dto)
