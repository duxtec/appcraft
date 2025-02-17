import os
from appcraft.utils.template_abc import TemplateABC


class DataVisualizationTemplate(TemplateABC):
    @property
    def description(self):
        return """
Data Visualization Template provides templates and libraries for creating \
insightful data visualizations. It supports the creation of various chart \
types and visual representations of data, helping users to gain better \
insights into their data through visual means.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('data_visualization/visualization.py')
        directory_exists = os.path.isdir('data_visualization')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
