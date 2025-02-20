from core.app import App
from services.browser.google import Google

class OpenGoogle(App):
    
    @App.runner
    def runner(self):
        google = Google()
        google.open()
        print(f"Page Title: {google.title}")
        input("Press Enter to close the browser...")
            

