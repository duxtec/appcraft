import os
from appcraft.utils.template_abc import TemplateABC


class MachineLearningTemplate(TemplateABC):
    @property
    def description(self):
        return """
Machine Learning Template provides the necessary tools and configurations for \
developing machine learning models. It includes libraries, scripts for \
training models, and configurations for processing data and making predictions.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('machine_learning/train_model.py')
        directory_exists = os.path.isdir('machine_learning')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
