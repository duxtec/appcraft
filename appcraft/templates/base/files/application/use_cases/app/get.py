from application.mappers.app import AppMapper
from application.providers.app import IAppProvider
from application.schemas.output.app import AppSchema


class GetAppUseCase:
    def __init__(self, app_provider: IAppProvider):
        self.provider = app_provider

    def execute(self) -> AppSchema:
        app = self.provider.get()
        return AppMapper.to_schema(app)
