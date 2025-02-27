import os

import pandas as pd


class Files:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def getExcel(self, file_name, sheet_name=0):
        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"
        file_path = os.path.join(self.folder_path, file_name)
        df = pd.read_excel(file_path, engine="openpyxl", sheet_name=sheet_name)
        return df
