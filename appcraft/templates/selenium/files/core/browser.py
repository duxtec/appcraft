from browser_manager import BrowserManager
from browser_manager.browser import Browser, Chrome, Chromium, Firefox, IExplore, MSEdge, Opera, Safari
from core.base.config import Config

class Browser:
    def __init__(self):
        config = Config().get("browser", "browser")
        browser_name = config.get("browser")
        profile = config.get("profile")
        headless = config.get("headless")

        browser_classes = {
            "Chrome": Chrome,
            "Chromium": Chromium,
            "Firefox": Firefox,
            "IExplore": IExplore,
            "MSEdge": MSEdge,
            "Opera": Opera,
            "Safari": Safari
        }

        browser_class = self.get_browser_class(browser_name, browser_classes)

        browser_manager = BrowserManager()
        browser = browser_manager.select_browser(browser_class)

        browser.select_profile(profile)

        options = browser._options()

        if headless:
            try:
                options.add_argument("--headless")
            except:
                options.headless = True
        
        self.driver = browser.get_driver(options)

    def get_browser_class(self, browser_name, browser_classes) -> Browser:
        browser_class = browser_classes.get(browser_name)
        if not browser_class:
            raise ValueError(f"Navegador '{browser_name}' não é suportado.")
        return browser_class
