import sys
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                             QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from calcs import parse_single_function, root_counter

MAX_INTERVAL_LENGTH = 1000000

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.left_border = -1
        self.right_border = 1
        self.accuracy = 0.05
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 600, 600)

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

        self.draw_graph_button = QPushButton("Построить", self)
        self.draw_graph_button.clicked.connect(self.draw_graph)
        layout.addWidget(self.draw_graph_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        self.result_table = QTableWidget(0, 2)
        self.result_table.setHorizontalHeaderLabels(["Метод", "Найденный корень"])
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def validate_fields(self):
        try:
            left_border = float(self.left_border_input.text().replace(",", ".")) if self.left_border_input.text() else self.left_border
            right_border = float(self.right_border_input.text().replace(",",".")) if self.right_border_input.text() else self.right_border
            accuracy = float(self.accuracy_input.text().replace(",", ".")) if self.accuracy_input.text() else self.accuracy

            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого.")
                return False
            if right_border - left_border > MAX_INTERVAL_LENGTH:
                self.show_error("Ошибка диапазона", "Выбран слишком широкий интервал.")
                return False
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом.")
                return False

            self.left_border = left_border
            self.right_border = right_border
            self.accuracy = accuracy
            return True
        except:
            self.show_error("Ошибка диапазона", "Балду какую-то вводишь братик")
            return False


    def draw_graph(self):
        function_text = self.function_input.text().strip()
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return

        f = parse_single_function(function_text)
        if f is None:
            self.show_error("Ошибка", "Некорректная функция")
            return

        try:
            if self.validate_fields():
                x_sym = sp.symbols('x')
                self.func = sp.lambdify(x_sym, f, 'numpy')
                x_vals = np.linspace(self.left_border, self.right_border, 400)
                try:
                    y_vals = self.func(x_vals)
                except (OverflowError, ValueError, TypeError) as e:
                    self.show_error("Ошибка вычисления", "Функция принимает слишком большие значения. Измените интервал.")
                    return
                self.ax.clear()
                self.ax.plot(x_vals, y_vals, label=function_text)
                self.ax.axhline(0, color='black', linewidth=0.5)
                self.ax.axvline(0, color='black', linewidth=0.5)
                self.ax.legend()
                self.canvas.draw()

        except Exception as e:
            self.show_error("Ошибка", f"Ошибка при вычислении: {str(e)}")

    def calculate(self):

        if self.validate_fields():
            root_amount = root_counter(self.left_border, self.right_border, self.func)
            if root_amount > 1:
                self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, содержащий только 1 корень.")
                return

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