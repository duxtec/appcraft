from application.dtos.app_dto import AppDTO
from domain.models.app import App


class AppMapper:
    @staticmethod
    def to_dto(app: App):
        return AppDTO(
            name=app.name,
            version=app.version,
            environment=app.environment,
            debug_mode=app.debug_mode,
        )

    @staticmethod
    def to_domain(app_dto: AppDTO):
        return App(
            name=app_dto.name,
            version=app_dto.version,
            environment=app_dto.environment,
            debug_mode=app_dto.debug_mode
        )
