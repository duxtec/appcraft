import importlib
from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from infrastructure.framework.appcraft.utils.printer import Printer


class FlaskSQLAlchemy:
    def __init__(self, app: Flask):
        # sqlalchemy is an optional template — its files only exist in the
        # generated project when installed, so this can't be a static
        # top-level import without breaking pyright for every flask
        # project that doesn't also install sqlalchemy. Same pattern as
        # application/providers/adapters/database.py.
        #
        # Uses the sqlalchemy-specific singleton (not
        # get_default_database_adapter()) so this keeps working even when
        # another database template (e.g. mongodb) is configured as the
        # project's default adapter — Flask-SQLAlchemy always needs a real
        # SQLAlchemyAdapter, never whichever backend happens to be default.
        base_module = importlib.import_module(
            "infrastructure.database.sqlalchemy.models.base"
        )
        adapter_module = importlib.import_module(
            "infrastructure.database.sqlalchemy.adapter"
        )

        self.db = SQLAlchemy(model_class=base_module.Base)
        self.adapter: Any = adapter_module.get_sqlalchemy_adapter()
        self.app = app

    def init_app(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.adapter.uri
        self.db.init_app(self.app)
        with self.app.app_context():
            if not self.adapter.inspector.get_table_names():
                self.db.create_all()

            self.db.session.execute(text("SELECT 1"))
            Printer.success("Successfully connected database!")

        # From this point on, the adapter delegates session management
        # to Flask-SQLAlchemy's request-scoped session — same adapter,
        # same DatabasePort contract, now with per-request lifecycle.
        self.adapter.use_external_session(self.db.session)
