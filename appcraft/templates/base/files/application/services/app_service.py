from application.dtos.app_dto import AppDTO
from application.mappers.app_mapper import AppMapper
from infrastructure.memory.adapters.interfaces.app_adapter_interface import (
    AppAdapterInterface,
)


class AppService:
    def __init__(self, app_adapter: AppAdapterInterface):
        self.adapter = app_adapter

    def get_app(self) -> AppDTO:
        app = self.adapter.get()
        app_dto = AppMapper.to_dto(app)
        return app_dto
