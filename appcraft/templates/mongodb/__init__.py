from ..template_abc import TemplateABC


class MongoDBTemplate(TemplateABC):
    active = True
    description = "\
MongoDB Template provides a DatabasePort adapter backed by MongoDB \
(via pymongo). It can be installed on its own, replacing the in-memory \
default, or alongside the sqlalchemy template — config/app.toml's \
default_database_adapter picks which one backs get_default_database_adapter() \
when both are installed, and repositories that specifically want document \
storage can inject MongoDBAdapter directly regardless of that default."
