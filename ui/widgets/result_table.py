from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class ResultTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 4, parent)
        self.setHorizontalHeaderLabels(["Метод", "Количество итераций", "Найденный корень", "Значение функции"])
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

    def update_result_table_solo(self, results):
        self.setHorizontalHeaderLabels(["Метод", "Количество итераций", "Найденный корень", "Значение функции"])
        self.clearContents()
        self.setRowCount(0)
        self.setRowCount(len(results))

        for row, (method, data) in enumerate(results):
            self.setItem(row, 0, QTableWidgetItem(method))
            self.setItem(row, 1, QTableWidgetItem(str(data["iter_amount"]) if data["status_msg"] == "OK" else data["status_msg"]))
            self.setItem(row, 2, QTableWidgetItem("Не найден" if data['root'] is None else f"{data['root']:.15f}"))
            self.setItem(row, 3, QTableWidgetItem("Метод не применим" if data['value'] is None else f"{data['value']:.15f}"))
        self.resizeColumnsToContents()

    def update_result_table_system(self, results):
        self.setHorizontalHeaderLabels(["Метод", "Количество итераций", "Значение X", "Значение Y"])
        self.clearContents()
        self.setRowCount(0)
        self.setRowCount(len(results))
        print(results)
        for row, (method, data) in enumerate(results):
            self.setItem(row, 0, QTableWidgetItem(method))
            self.setItem(row, 1, QTableWidgetItem(str(data["iter_amount"]) if data["status_msg"] == "OK" else data["status_msg"]))
            self.setItem(row, 2, QTableWidgetItem("Не найден" if data['root'] is None else f"{data['root']:.15f}"))
            self.setItem(row, 3, QTableWidgetItem("Не найден" if data['value'] is None else f"{data['value']:.15f}"))
        self.resizeColumnsToContents()

    def clear_table(self):
        self.clearContents()
        self.setRowCount(0)