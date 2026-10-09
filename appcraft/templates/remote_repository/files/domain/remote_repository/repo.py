from dataclasses import dataclass


@dataclass(frozen=True)
class RemoteRepo:
    name: str
    url: str
    description: str
    is_private: bool
