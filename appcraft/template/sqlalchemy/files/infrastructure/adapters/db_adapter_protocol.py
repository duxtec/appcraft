from typing import List, Protocol


class DbAdapterProtocol(Protocol):
    def get_session(self):
        ...

    def get_tables(self) -> List[str]:
        ...
