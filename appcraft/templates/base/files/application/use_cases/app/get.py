from application.mappers.app import AppMapper
from application.ports.app import AppPort
from application.schemas.output.app import AppSchema


class GetAppUseCase:
    def __init__(self, app_provider: AppPort):
        self.provider = app_provider

    def execute(self) -> AppSchema:
        app = self.provider.get()
        return AppMapper.to_schema(app)
