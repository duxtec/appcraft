from abc import ABC

from application.interfaces.adapters import ReaderWriterAdapterInterface


class DatabaseAdapterInterface(ReaderWriterAdapterInterface, ABC):
    pass
