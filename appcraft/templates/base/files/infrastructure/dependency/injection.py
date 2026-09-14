import inspect

from injector import Binder, Module, ScopeDecorator, inject, singleton

from application.ports.database import DatabasePort
from application.providers.adapters.database import (
    get_default_database_adapter,
)
from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)


class ApplicationModule(Module):
    def configure(self, binder: Binder):
        self._bind_database(binder)
        self._bind_repositories(binder)
        self._bind_use_cases(binder)

    def _bind_database(self, binder: Binder):
        binder.bind(
            DatabasePort,
            to=get_default_database_adapter(),
            scope=singleton,
        )

    def _bind_repositories(self, binder: Binder):
        repositories = ImportManager(
            "application.repositories"
        ).get_module_attributes(recursive=True)

        self._bind_classes(binder, repositories, singleton)

    def _bind_use_cases(self, binder: Binder):
        use_cases = ImportManager(
            "application.use_cases"
        ).get_module_attributes(recursive=True)

        self._bind_classes(binder, use_cases, singleton)

    def _bind_classes(
        self,
        binder: Binder,
        attributes: dict[str, object],
        scope: ScopeDecorator,
    ):
        for attr in attributes.values():
            if inspect.isclass(attr):
                if "__init__" in attr.__dict__:
                    attr.__init__ = inject(attr.__init__)

                binder.bind(
                    attr,
                    to=attr,
                    scope=scope,
                )
            elif isinstance(attr, dict):
                self._bind_classes(binder, attr, scope)  # type: ignore
