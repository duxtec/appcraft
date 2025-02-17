import os
from typing import Dict, List, Optional
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from infrastructure.adapters.db_adapter_protocol import DbAdapterProtocol
from infrastructure.framework.appcraft.base.config import Config
from infrastructure.database.models.base import Base
from infrastructure.framework.appcraft.utils.import_manager \
    import ImportManager


class SqlAdapter(DbAdapterProtocol):
    def __init__(self, db_uri: Optional[str] = None):
        self.config = Config().get("database")
        self.uri = db_uri or self.config['SQLALCHEMY_DATABASE_URI']
        self.engine = create_engine(self.uri)

        ImportManager(
            "infrastructure.database.models"
        ).get_module_attributes()

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

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
                    current_dir, 'infrastructure', 'database'
                )
                os.makedirs(db_dir, exist_ok=True)
                db_file = os.path.join(db_dir, db_file)

            self.__uri = f'sqlite:///{db_file}'
        else:
            self.__uri = db_uri

    def get_tables(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def get_columns(self, table_name: str) -> List[Dict]:
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        return columns
