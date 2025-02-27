from typing import TypeVar

from domain.interfaces.repositories import RepositoryInterface

RepositoryType = TypeVar('RepositoryType', bound=RepositoryInterface)
