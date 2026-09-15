from typing import TypeVar

from application.ports import Port

TPort = TypeVar('TPort', bound=Port)
