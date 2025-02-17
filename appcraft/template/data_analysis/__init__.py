import os
from appcraft.utils.template_abc import TemplateABC


class DataAnalysisTemplate(TemplateABC):
    @property
    def description(self):
        return """
Data Analysis Template provides resources and configurations for performing \
data analysis tasks. It includes tools for data processing, cleaning, and \
transforming, making it easier to analyze and visualize large datasets. \
This template is ideal for data scientists and analysts.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('data_analysis/analysis.py')
        directory_exists = os.path.isdir('data_analysis')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
