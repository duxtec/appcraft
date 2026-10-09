from application.mappers import MapperBase
from application.schemas.output.app import AppSchema
from domain.models.app import App


class AppMapper(MapperBase[App, AppSchema]):
    pass
