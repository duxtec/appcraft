from application.mappers.bases import BaseMapper
from application.schemas.output.app import AppSchema
from domain.models.app import App


class AppMapper(BaseMapper[App, AppSchema]):
    pass
