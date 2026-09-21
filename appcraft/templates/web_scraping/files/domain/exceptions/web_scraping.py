class WebScrapingException(RuntimeError):
    pass


class NoSuchElementException(WebScrapingException):
    def __init__(self, selector: str | None = None):
        if selector:
            message = f"Element `{selector}` not found"
        else:
            message = "Element not found"

        super().__init__(message)


class BrowserNotInstalledException(WebScrapingException):
    def __init__(self, browser_name: str, *args: object) -> None:
        if not args:
            args = (
                f"""\
The browser '{browser_name}' does not installed.""",
            )

        super().__init__(*args)


class NoBrowsersInstalledException(WebScrapingException):
    def __init__(self, *args: object) -> None:
        if not args:
            args = (
                """\
No supported browsers are installed on this system.
Please install a supported browser and try again.""",
            )

        super().__init__(*args)
