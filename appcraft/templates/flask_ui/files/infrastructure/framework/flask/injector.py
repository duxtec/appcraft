import inspect

from flask_injector import request
from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)
from injector import Module, singleton


class FlaskInjector(Module):
    def inject_services(self, binder):
        service_modules = ImportManager(
            "domain.services"
        ).get_module_attributes()

        for module_name, module in service_modules.items():
            for attr_name, attr in module.__dict__.items():
                if inspect.isclass(attr):
                    binder.bind(attr, to=attr, scope=request)

    def inject_repositories(self, binder):
        repository_modules = ImportManager(
            "infrastructure.memory.repositories"
        ).get_module_attributes()

        for module_name, module in repository_modules.items():
            for attr_name, attr in module.__dict__.items():
                if inspect.isclass(attr):
                    binder.bind(attr, to=attr, scope=singleton)
