from application.dtos.app_dto import AppDTO
from application.mappers.bases import BaseMapper
from domain.models.app import App


class AppMapper(BaseMapper[App, AppDTO]):
    pass
