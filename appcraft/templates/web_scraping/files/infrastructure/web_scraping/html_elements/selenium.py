from typing import Self

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from domain.interfaces.html_element.html_element import (
    IHTMLInteractiveElement,
)


class SeleniumHTMLElement(IHTMLInteractiveElement):
    def __init__(self, element: WebElement, timeout: float = 5) -> None:
        self._element = element
        self._driver: WebDriver = element.parent
        self._timeout = timeout
        self._wait = WebDriverWait(element, self._timeout)

    @property
    def inner_html(self) -> str:
        inner_html = self._element.get_attribute("innerHTML")  # type: ignore
        if not inner_html:
            inner_html = ""
        return inner_html

    @inner_html.setter
    def inner_html(self, value: str | Self):
        self._driver.execute_script(  # type: ignore
            "arguments[0].innerHTML = arguments[1];", self._element, value
        )

    @property
    def inner_text(self) -> str:
        return self._element.text

    def has_attribute(self, name: str) -> bool:
        if self._element.get_attribute(name) is None:  # type: ignore
            return False
        return True

    def get_attribute(self, name: str) -> str | None:
        return self._element.get_attribute(name)  # type: ignore

    def set_attribute(self, name: str, value: str):
        self._driver.execute_script(  # type: ignore
            "arguments[0].setAttribute(arguments[1], arguments[2]);",
            self._element,
            name,
            value,
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
            self._driver.execute_script(  # type: ignore
                "arguments[0].removeAttribute(arguments[1]);",
                self._element,
                name,
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
        self._driver.execute_script(  # type: ignore
            "arguments[0].appendChild(arguments[1]);", self._element, child
        )

    def remove_child(self, child: Self | int):
        if isinstance(child, int):
            self._driver.execute_script(  # type: ignore
                "\
arguments[0].removeChild(arguments[0].children[arguments[1]]);",
                self._element,
                child,
            )
        else:
            self._driver.execute_script(  # type: ignore
                "arguments[0].removeChild(arguments[1]);",
                self._element,
                child._element,
            )

    def send_keys(self, *value: str):
        self._element.send_keys(*value)

    def click(self) -> None:
        self._element.click()

    def hover(self) -> None:
        actions = ActionChains(self._driver)
        actions.move_to_element(self._element).perform()

    def focus(self) -> None:
        self._driver.execute_script(  # type: ignore
            "arguments[0].focus();", self._element
        )

    def blur(self) -> None:
        """Remove o foco do elemento utilizando JavaScript."""
        self._driver.execute_script(  # type: ignore
            "arguments[0].blur();", self._element
        )

    def remove(self) -> None:
        self._driver.execute_script(  # type: ignore
            "arguments[0].remove();", self._element
        )

    def query_selector(self, selector: str) -> Self:
        element = self._wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return self.__class__(element)

    def query_selector_all(self, selector: str) -> list[Self]:
        elements = self._wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return [self.__class__(el) for el in elements]

    @property
    def children(self) -> list[Self]:
        return self.query_selector_all(":scope > *")
