from core.base.config import Config
from flask import Flask

from .routes import page_bp


def create_app():
    app = Flask(__name__, static_folder="app/assets", static_url_path="/assets")

    # Registro dos Blueprints
    app.register_blueprint(page_bp)

    config = Config().get("database", "database")

    if config and "SQLALCHEMY_DATABASE_URI" in config:
        app = database_app(app)

    return app


def database_app(app):
    from core.database import Database
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import text

    database = Database()
    # Inicializa o objeto SQLAlchemy sem associar a nenhum app ainda
    db = SQLAlchemy()

    db_config = database.config

    app.config.update(db_config)

    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    # Com o app.app_context(), você pode criar as tabelas no banco de dados
    with app.app_context():
        if not self.inspector.get_table_names():
            db.create_all()  # Cria as tabelas se elas ainda não existirem
        try:
            # Verifica se é possível estabelecer conexão com o banco de dados
            db.session.execute(text("SELECT 1"))
            print("Successfully connected database!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    return app
