from infrastructure.database.sqlalchemy.models.base import Base
from sqlalchemy import Boolean, Column, String


class AppDB(Base):
    __tablename__ = "apps"

    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    debug_mode = Column(Boolean, nullable=False)
    log_level = Column(String, nullable=False)
    language = Column(String, nullable=False)
    language_preference = Column(String, nullable=False)
    supported_languages = Column(String, nullable=False)

    def __init__(
        self,
        name: str,
        version: str,
        environment: str,
        debug_mode: bool,
        log_level: str,
        language: str,
        language_preference: str,
        supported_languages: list,
    ):
        self.name = name
        self.version = version
        self.environment = environment
        self.debug_mode = debug_mode
        self.log_level = log_level
        self.language = language
        self.language_preference = language_preference
        self.supported_languages = ",".join(supported_languages)

    def __repr__(self):
        return (
            f"App(id={self.id}, name={self.name}, version={self.version}, "
            f"environment={self.environment}, debug_mode={self.debug_mode}, "
            f"log_level={self.log_level}, language={self.language}, "
            f"language_preference={self.language_preference}, "
            f"supported_languages={self.supported_languages})"
        )

    @property
    def supported_languages_list(self):
        return self.supported_languages.split(",")

    @supported_languages_list.setter
    def supported_languages_list(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Supported languages must be a list")
        if len(value) == 0:
            raise ValueError("Supported languages list cannot be empty")
        self.supported_languages = ",".join(value)
