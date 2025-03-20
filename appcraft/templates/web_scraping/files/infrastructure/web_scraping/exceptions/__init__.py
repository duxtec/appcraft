class WebScrapingException(Exception):
    pass


class NoSuchElementException(WebScrapingException):
    def __init__(self, selector: str | None = None):
        if selector:
            message = f"Element `{selector}` not found"
        else:
            message = "Element not found"

        super().__init__(message)
