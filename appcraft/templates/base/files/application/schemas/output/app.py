from application.schemas import Schema
from domain.app import Environment


class AppSchema(Schema):
    name: str
    version: str
    environment: Environment
    debug_mode: bool
