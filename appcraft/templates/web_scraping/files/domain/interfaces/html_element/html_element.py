from abc import ABC, abstractmethod
from typing import Self, Sequence


class IHTMLElement(ABC):
    pass


class IHTMLReadingElement(IHTMLElement, ABC):
    @property
    @abstractmethod
    def inner_html(self) -> str:
        pass

    @property
    @abstractmethod
    def inner_text(self) -> str:
        pass

    @abstractmethod
    def has_attribute(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_attribute(self, name: str) -> str | None:
        pass


class IHTMLNavigationElement(IHTMLReadingElement, ABC):
    @abstractmethod
    def query_selector(self, selector: str) -> Self:
        pass

    @abstractmethod
    def query_selector_all(self, selector: str) -> Sequence[Self]:
        pass

    @property
    @abstractmethod
    def children(self) -> list[Self]:
        pass


class IHTMLInteractiveElement(IHTMLNavigationElement, ABC):
    @property
    @abstractmethod
    def inner_html(self) -> str:
        pass

    @inner_html.setter
    @abstractmethod
    def inner_html(self, value: str | Self):
        pass

    @property
    @abstractmethod
    def inner_text(self) -> str:
        pass

    @abstractmethod
    def set_attribute(self, name: str, value: str):
        pass

    @abstractmethod
    def add_attribute(self, name: str, value: str):
        pass

    @abstractmethod
    def remove_attribute(self, name: str, value: str):
        pass

    @abstractmethod
    def append_child(self, child: Self):
        pass

    @abstractmethod
    def remove_child(self, child: Self | int):
        pass

    @abstractmethod
    def send_keys(self, *value: str):
        pass

    @abstractmethod
    def click(self) -> None:
        pass

    @abstractmethod
    def hover(self) -> None:
        pass

    @abstractmethod
    def focus(self) -> None:
        pass

    @abstractmethod
    def blur(self) -> None:
        pass

    @abstractmethod
    def remove(self) -> None:
        pass
