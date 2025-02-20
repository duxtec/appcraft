from abc import ABC, abstractmethod
from typing import List


class DbAdapterInterface(ABC):
    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def get_tables(self) -> List[str]:
        pass
