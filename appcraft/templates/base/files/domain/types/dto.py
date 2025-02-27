from typing import TypeVar

from application.dtos.interfaces import DTOInterface

DTOType = TypeVar('DTOType', bound=DTOInterface)
