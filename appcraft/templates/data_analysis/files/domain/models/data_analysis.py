from typing import List, Dict


class DataSet:
    def __init__(self, data: List[Dict]):
        self.data = data

    def get_data(self):
        return self.data


class DataSummary(DataSet):
    def __init__(self, data: List[Dict]):
        super().__init__(data)

    def summarize(self):
        summary = {
            "total_records": len(self.data),
            "columns": list(self.data[0].keys()) if self.data else []
        }
        return summary


class CorrelationAnalysis(DataSet):
    def __init__(self, data: List[Dict]):
        super().__init__(data)

    def calculate_correlation(self):
        correlation = {col: 0.75 for col in self.data[0].keys()}
        return correlation


class DataCleaning(DataSet):
    def __init__(self, data: List[Dict]):
        super().__init__(data)

    def clean_missing_values(self, threshold: float = 0.5):
        cleaned_data = [
            {key: value for key, value in record.items() if value is not None}
            for record in self.data
        ]
        return cleaned_data


class FeatureEngineering(DataSet):
    def __init__(self, data: List[Dict]):
        super().__init__(data)

    def create_feature(self, column1: str, column2: str, new_column_name: str):
        for record in self.data:
            record[new_column_name] = record[column1] + record[column2]
        return self.data
