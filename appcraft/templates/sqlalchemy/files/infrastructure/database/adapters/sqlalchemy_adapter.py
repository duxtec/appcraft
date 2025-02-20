import os
from typing import Dict, List, Optional

from domain.adapters.db_adapter_interface import DbAdapterInterface
from infrastructure.database.sqlalchemy.models.base import Base
from infrastructure.framework.appcraft.core.config import Config
from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


class SqlAlchemyAdapter(DbAdapterInterface):

    def __init__(self, db_uri: Optional[str] = None, create_all=True):

        self.config = Config().get("database")
        self.__uri = db_uri or self.config["SQLALCHEMY_DATABASE_URI"]
        self.engine = create_engine(self.uri)
        self.inspector = inspect(self.engine)

        if not self.inspector.get_table_names() and create_all:
            Base.metadata.create_all(self.engine)

        ImportManager(
            "infrastructure.database.sqlalchemy.models"
        ).get_module_attributes()

        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, db_uri):
        if not db_uri:
            raise ValueError("Database URI cannot be empty.")

        if db_uri.startswith("sqlite:///"):
            db_file = db_uri.replace("sqlite:///", "")

            if not os.path.isabs(db_file):
                current_dir = os.getcwd()
                db_dir = os.path.join(
                    current_dir, "infrastructure", "database"
                )
                os.makedirs(db_dir, exist_ok=True)
                db_file = os.path.join(db_dir, db_file)

            self.__uri = f"sqlite:///{db_file}"
        else:
            self.__uri = db_uri

    def get_tables(self):
        return self.inspector.get_table_names()

    def get_columns(self, table_name: str) -> List[Dict]:
        columns = self.inspector.get_columns(table_name)
        return columns
