import sys
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                             QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from test import parse_function


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 600, 600)

        self.left_border = -1
        self.right_border = 1
        self.accuracy = 0.05

        layout = QVBoxLayout()

        self.function_input = QLineEdit(self)
        self.function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        layout.addWidget(self.function_input)

        self.left_border_input = QLineEdit(self)
        self.right_border_input = QLineEdit(self)
        self.accuracy_input = QLineEdit(self)

        validator = QDoubleValidator()
        self.left_border_input.setValidator(validator)
        self.right_border_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)

        self.left_border_input.setPlaceholderText("Левый предел")
        self.right_border_input.setPlaceholderText("Правый предел")
        self.accuracy_input.setPlaceholderText("Точность")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.left_border_input)
        input_layout.addWidget(self.right_border_input)
        input_layout.addWidget(self.accuracy_input)
        layout.addLayout(input_layout)

        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.result_table = QTableWidget(0, 2)
        self.result_table.setHorizontalHeaderLabels(["Метод", "Найденный корень"])
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def calculate(self):
        function_text = self.function_input.text()
        print(f"Функция: {function_text}")  # 🛠 Отладка

        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return

        func = parse_function(function_text)
        if func is None:
            self.show_error("Ошибка", f"Некорректная функция: {error}")
            return

        try:
            left_border = float(
                self.left_border_input.text().replace(",", ".")) if self.left_border_input.text() else self.left_border
            right_border = float(self.right_border_input.text().replace(",",
                                                                        ".")) if self.right_border_input.text() else self.right_border
            accuracy = float(
                self.accuracy_input.text().replace(",", ".")) if self.accuracy_input.text() else self.accuracy

            print(f"Левый предел: {left_border}, Правый предел: {right_border}, Точность: {accuracy}")  # 🛠 Отладка

            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого!")
                return
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом!")
                return

            self.left_border = left_border
            self.right_border = right_border
            self.accuracy = accuracy

            # Отрисовка графика
            x = np.linspace(self.left_border, self.right_border, 400)
            print(f"x: {x[:5]} ... {x[-5:]}")  # 🛠 Отладка

            y = func(x)  # Вычисление значений функции
            print(f"y: {y[:5]} ... {y[-5:]}")  # 🛠 Отладка

            self.ax.clear()
            self.ax.plot(x, y, label=function_text)
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            print(f"Ошибка: {str(e)}")  # 🛠 Отладка
            self.show_error("Ошибка", f"Ошибка при вычислениях: {str(e)}")

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
