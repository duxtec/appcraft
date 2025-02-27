from application.dtos.app_dto import AppDTO
from application.interfaces.adapters.app_adapter import AppAdapterInterface
from application.mappers.app_mapper import AppMapper


class AppService:
    def __init__(self, app_adapter: AppAdapterInterface):
        self.adapter = app_adapter

    def get_app(self) -> AppDTO:
        app = self.adapter.get()
        app_dto = AppMapper.to_dto(app)
        return app_dto
