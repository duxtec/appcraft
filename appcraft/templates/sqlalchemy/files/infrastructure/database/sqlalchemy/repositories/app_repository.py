from domain.models.app import App
from infrastructure.database.sqlalchemy.models.app_db import AppDB
from sqlalchemy.orm import Session


class AppRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, app: App) -> None:
        app_db = AppDB(
            name=app.name,
            version=app.version,
            environment=app.environment,
            debug_mode=app.debug_mode,
            log_level=app.log_level,
            language=app.language,
            language_preference=app.language_preference,
            supported_languages=",".join(app.supported_languages),
        )
        self.session.add(app_db)
        self.session.commit()

    def get_by_id(self, app_id: int) -> App:
        app_db = self.session.query(AppDB).filter_by(id=app_id).first()
        if app_db:
            return App(
                id=app_db.id,
                name=app_db.name,
                version=app_db.version,
                environment=app_db.environment,
                debug_mode=app_db.debug_mode,
                log_level=app_db.log_level,
                language=app_db.language,
                language_preference=app_db.language_preference,
                supported_languages=app_db.supported_languages.split(","),
            )
        return None

    def get_all(self) -> list[App]:
        apps_db = self.session.query(AppDB).all()
        return [
            App(
                id=app_db.id,
                name=app_db.name,
                version=app_db.version,
                environment=app_db.environment,
                debug_mode=app_db.debug_mode,
                log_level=app_db.log_level,
                language=app_db.language,
                language_preference=app_db.language_preference,
                supported_languages=app_db.supported_languages.split(","),
            )
            for app_db in apps_db
        ]
