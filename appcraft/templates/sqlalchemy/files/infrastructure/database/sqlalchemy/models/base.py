from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
import datetime


class Base(declarative_base()):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
