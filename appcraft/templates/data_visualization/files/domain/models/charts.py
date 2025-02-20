from typing import List, Dict


class Chart:
    def __init__(self, title: str, data: List[Dict]):
        self.title = title
        self.data = data

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data


class BarChart(Chart):
    def __init__(
        self, title: str, data: List[Dict],
        x_column: str, y_column: str
    ):
        super().__init__(title, data)
        self.x_column = x_column
        self.y_column = y_column

    def plot(self):
        # Aqui você faria a implementação real para gerar o gráfico
        print(f"\
Plotting Bar Chart: {self.get_title()} using \
{self.x_column} and {self.y_column}")


class LineChart(Chart):
    def __init__(
        self, title: str, data: List[Dict], x_column: str, y_column: str
    ):
        super().__init__(title, data)
        self.x_column = x_column
        self.y_column = y_column

    def plot(self):
        # Implementação real do gráfico de linha
        print(f"\
Plotting Line Chart: {self.get_title()} using {self.x_column} \
and {self.y_column}")


class PieChart(Chart):
    def __init__(self, title: str, data: List[Dict], category_column: str):
        super().__init__(title, data)
        self.category_column = category_column

    def plot(self):
        # Implementação real do gráfico de pizza
        print(f"\
Plotting Pie Chart: {self.get_title()} using {self.category_column}")
