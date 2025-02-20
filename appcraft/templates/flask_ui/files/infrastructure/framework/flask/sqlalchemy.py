from flask_sqlalchemy import SQLAlchemy
from infrastructure.adapters.sql_adapter import SqlAdapter
from infrastructure.database.models.base import Base
from infrastructure.framework.appcraft.utils.printer import Printer
from sqlalchemy import text


class FlaskSQLAlchemy:
    def __init__(self, app):
        self.db = SQLAlchemy(model_class=Base)
        self.adapter = SqlAdapter()
        self.app = app

    def init_app(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.adapter.uri
        self.db.init_app(self.app)
        with self.app.app_context():
            if not self.adapter.inspector.get_table_names():
                self.db.create_all()

            self.db.session.execute(text("SELECT 1"))
            Printer.success("Successfully connected database!")
