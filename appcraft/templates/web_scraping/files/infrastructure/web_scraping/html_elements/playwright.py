from typing import Self

from playwright.sync_api import ElementHandle, Page

from domain.interfaces.html_element.html_element import (
    IHTMLInteractiveElement,
)
from infrastructure.web_scraping.exceptions import NoSuchElementException
from infrastructure.web_scraping.utils.keys import Keys


class PlaywrightHTMLElement(IHTMLInteractiveElement):
    def __init__(
        self, element: ElementHandle, page: Page, timeout: float = 5
    ) -> None:
        self._element = element
        self._page = page
        self._timeout = timeout

    @property
    def inner_html(self) -> str:
        return self._element.inner_html()

    @inner_html.setter
    def inner_html(self, value: str | Self):
        self._page.evaluate(
            "(element, value) => element.innerHTML = value",
            [
                self._element,
                value,
            ],
        )

    @property
    def inner_text(self) -> str:
        return self._element.inner_text()

    def has_attribute(self, name: str) -> bool:
        return self._element.get_attribute(name) is not None

    def get_attribute(self, name: str) -> str | None:
        return self._element.get_attribute(name)

    def set_attribute(self, name: str, value: str):
        self._page.evaluate(
            "(element, name, value) => element.setAttribute(name, value)",
            [
                self._element,
                name,
                value,
            ],
        )

    def add_attribute(self, name: str, value: str):
        attribute = self.get_attribute(name)
        if attribute:
            attributes = attribute.split(" ")
            if value not in attributes:
                attributes.append(value)
            value = " ".join(attributes)

        self.set_attribute(name, value)

    def remove_attribute(self, name: str, value: str | None = None):
        if not value:
            self._page.evaluate(
                "(element, name) => element.removeAttribute(name)",
                [
                    self._element,
                    name,
                ],
            )
            return

        attribute = self.get_attribute(name)

        if attribute is None:
            return

        attributes = attribute.split(" ")

        if value in attributes:
            attributes.remove(value)

        attribute = " ".join(attributes)

        self.set_attribute(name, attribute)

    def append_child(self, child: Self):
        self._page.evaluate(
            "(parent, child) => parent.appendChild(child)",
            [
                self._element,
                child._element,
            ],
        )

    def remove_child(self, child: Self | int):
        if isinstance(child, int):
            self._page.evaluate(
                "\
(parent, index) => parent.removeChild(parent.children[index])",
                [
                    self._element,
                    child,
                ],
            )
        else:
            self._page.evaluate(
                "(parent, child) => parent.removeChild(child)",
                [
                    self._element,
                    child._element,
                ],
            )

    def send_keys(self, *value: str):
        for v in value:
            key_name = self._get_key_name(v)

            if key_name:
                self._element.press(key_name)
            else:
                self._element.type(v)

    def _get_key_name(self, key_value: str) -> str | None:
        key_name = None
        for key in dir(Keys):
            if getattr(Keys, key) == key_value:
                key_name = key
                break
        if not key_name:
            return None

        valid_keys = [
            "Backspace",
            "Tab",
            "Enter",
            "Shift",
            "Control",
            "Alt",
            "Pause",
            "Escape",
            "Space",
            "PageUp",
            "PageDown",
            "End",
            "Home",
            "ArrowLeft",
            "ArrowUp",
            "ArrowRight",
            "ArrowDown",
            "Insert",
            "Delete",
            "Semicolon",
            "Equals",
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
            "F8",
            "F9",
            "F10",
            "F11",
            "F12",
            "Meta",
            "Command",
        ]

        for valid_key in valid_keys:
            if key_name.strip().lower() == valid_key.lower():
                return valid_key

        return None

    def click(self) -> None:
        self._element.click()

    def hover(self) -> None:
        self._element.hover()

    def focus(self) -> None:
        self._page.evaluate("(element) => element.focus()", self._element)

    def blur(self) -> None:
        self._page.evaluate("(element) => element.blur()", self._element)

    def remove(self) -> None:
        self._page.evaluate("(element) => element.remove()", self._element)

    def query_selector(self, selector: str) -> Self:
        element = self._element.wait_for_selector(
            selector, timeout=self._timeout * 1000
        )
        if element:
            return self.__class__(element, self._page)
        raise NoSuchElementException

    def query_selector_all(self, selector: str) -> list[Self]:
        self._element.wait_for_selector(
            selector, timeout=self._timeout * 1000
        )
        elements = self._element.query_selector_all(selector)
        return [self.__class__(el, self._page) for el in elements]

    @property
    def children(self) -> list[Self]:
        return self.query_selector_all(":scope > *")
