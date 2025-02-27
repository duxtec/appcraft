from typing import TypeVar

from application.interfaces.adapters import AdapterInterface

AdapterType = TypeVar('AdapterType', bound=AdapterInterface)
