from ..template_abc import TemplateABC


class WebScrapingTemplate(TemplateABC):
    active = True
    description = "\
Web Scraping Template provides a setup for extracting data from websites. \
It includes pre-configured scripts for web scraping, as well as libraries for \
parsing HTML and handling web requests."
