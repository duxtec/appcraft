from ..template_abc import TemplateABC


class SQLAlchemyTemplate(TemplateABC):
    active = True
    description = "\
SQLAlchemy Template provides a setup for integrating the SQLAlchemy ORM with \
your application. It includes configuration files for database connection, as \
well as predefined models for interacting with relational databases."
