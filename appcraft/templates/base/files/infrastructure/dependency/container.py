from typing import TypeVar

from injector import Injector

from infrastructure.dependency.injection import ApplicationModule

T = TypeVar("T")


class ApplicationContainer:
    _container = Injector([ApplicationModule()])

    @classmethod
    def get(cls, interface: type[T]) -> T:
        return cls._container.get(interface)
