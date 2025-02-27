from typing import TypeVar

from application.services.interfaces import ServiceInterface

ServiceType = TypeVar('ServiceType', bound=ServiceInterface)
