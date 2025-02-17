import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.base.config import Config
from database.models.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        self.config = Config().get("database", "database")
        self.uri = self.config['SQLALCHEMY_DATABASE_URI']
        self.uri = self.get_uri()
        self.engine = create_engine(self.uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.Session()
    
    def get_uri(self):
        # Se for SQLite, verifica o caminho
        if self.uri.startswith("sqlite:///"):
            # Remove o prefixo 'sqlite:///' para obter o caminho
            db_file = self.uri.replace("sqlite:///", "")

            # Se o caminho não for absoluto, ajusta
            if not os.path.isabs(db_file):
                # Obtém o diretório atual de execução
                current_dir = os.getcwd()
                # Define o caminho para a pasta "database" na raiz do projeto
                db_dir = os.path.join(current_dir, 'database')
                os.makedirs(db_dir, exist_ok=True)  # Cria a pasta "database" se não existir
                db_file = os.path.join(db_dir, db_file)  # Monta o caminho completo do arquivo

            self.uri = f'sqlite:///{db_file}'
        
        return self.uri

