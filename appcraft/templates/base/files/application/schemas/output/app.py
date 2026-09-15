from application.schemas import Schema


class AppSchema(Schema):
    name: str
    version: str
    environment: str
    debug_mode: bool
