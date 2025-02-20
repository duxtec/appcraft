# services/open_google.py

from core.browser import Browser

class Google:
    def __init__(self):
        # Inicializa o gerenciador de navegador
        self.browser = Browser()
        self.title = None

    def open(self):
        self.browser.driver.get("https://www.google.com")
        self.title = self.browser.driver.title

    def close(self):
        self.browser.driver.quit()
