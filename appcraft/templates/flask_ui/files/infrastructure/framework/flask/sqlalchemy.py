import inspect

from flask_sqlalchemy import SQLAlchemy
from infrastructure.database.adapters.sqlalchemy_adapter import (
    SqlAlchemyAdapter,
)
from infrastructure.database.sqlalchemy.models.base import Base
from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)
from infrastructure.framework.appcraft.utils.printer import Printer
from sqlalchemy import text


class FlaskSQLAlchemy:
    def __init__(self, app):
        self.db = SQLAlchemy(model_class=Base)
        self.adapter = SqlAlchemyAdapter()
        self.app = app

    def init_app(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.adapter.uri
        self.db.init_app(self.app)
        with self.app.app_context():
            if not self.adapter.inspector.get_table_names():
                self.db.create_all()

            self.db.session.execute(text("SELECT 1"))
            Printer.success("Successfully connected database!")

    def register_repositories(self, binder):
        repository_modules = ImportManager(
            "infrastructure.repositories"
        ).get_module_attributes()

        for module_name, module in repository_modules.items():
            for attr_name, attr in module.__dict__.items():
                if inspect.isclass(attr):
                    binder.bind(
                        attr,
                        to=attr(self.db.session),
                        scope=self.db.session,
                    )
