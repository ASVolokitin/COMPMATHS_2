import sys
import numpy as np
import sympy as sp
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                             QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QTextEdit)
from PyQt6.QtGui import QDoubleValidator, QColor
import pyqtgraph as pg

from calcs import parse_function, root_counter

MAX_INTERVAL_LENGTH = 1000000
SAMPLES_AMOUNT = 10000

class HintWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подсказки по вводу функции")
        self.setGeometry(500, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.hint_text = QTextEdit(self)
        self.hint_text.setReadOnly(True)  # Запрещаем редактирование
        self.hint_text.setPlainText(
            "Примеры ввода функций:\n\n"
            "1. Полиномы: x**2 - 4*x + 4\n"
            "2. Тригонометрические функции: sin(x) + cos(x)\n"
            "3. Экспоненты: exp(x) - 2\n"
            "4. Логарифмы: log(x) + 1\n"
            "5. Комбинированные: x**2 + sin(x) - exp(x)\n\n"
            "Допустимые операторы: +, -, *, /, ** (степень)\n"
            "Допустимые функции: sin, cos, tan, exp, log, sqrt и др.\n"
            "Используйте 'x' как переменную."
        )
        layout.addWidget(self.hint_text)

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

        # Поле для ввода функции
        self.function_input = QLineEdit(self)
        self.function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        layout.addWidget(self.function_input)

        # Поля для ввода границ и точности
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

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Кнопка для построения графика
        self.draw_graph_button = QPushButton("Построить", self)
        self.draw_graph_button.clicked.connect(self.draw_graph)
        button_layout.addWidget(self.draw_graph_button)

        self.hints_button = QPushButton("Подсказки по вводу", self)
        button_layout.addWidget(self.hints_button)
        self.hints_button.clicked.connect(self.show_hints)

        # Виджет для отображения графика (PyQtGraph)
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')  # Устанавливаем белый фон
        layout.addWidget(self.graph_widget)

        # Кнопка для вычисления корней
        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        # Таблица для отображения результатов
        self.result_table = QTableWidget(0, 2)
        self.result_table.setHorizontalHeaderLabels(["Метод", "Найденный корень"])
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def validate_fields(self):
        try:
            left_border = float(self.left_border_input.text().replace(",", ".")) if self.left_border_input.text() else self.left_border
            right_border = float(self.right_border_input.text().replace(",", ".")) if self.right_border_input.text() else self.right_border
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

        f = parse_function(function_text)
        if f is None:
            self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
            return

        try:
            if self.validate_fields():
                x_sym = sp.symbols('x')
                self.func = sp.lambdify(x_sym, f, 'numpy')
                x_vals = np.linspace(self.left_border, self.right_border, SAMPLES_AMOUNT)
                try:
                    y_vals = self.func(x_vals)
                except (OverflowError, ValueError, TypeError) as e:
                    self.show_error("Ошибка вычисления", "Функция принимает слишком большие значения. Измените интервал.")
                    return

                # Очищаем предыдущий график
                self.graph_widget.clear()

                # Настраиваем цвета осей и текста
                self.graph_widget.getAxis('left').setPen(pg.mkPen(color='k'))  # Черный цвет для оси Y
                self.graph_widget.getAxis('bottom').setPen(pg.mkPen(color='k'))  # Черный цвет для оси X
                self.graph_widget.getAxis('left').setTextPen(pg.mkPen(color='k'))  # Черный цвет для текста оси Y
                self.graph_widget.getAxis('bottom').setTextPen(pg.mkPen(color='k'))  # Черный цвет для текста оси X

                # Настраиваем сетку
                self.graph_widget.showGrid(x=True, y=True, alpha=0.5)
                self.graph_widget.getViewBox().setBackgroundColor('w')  # Белый фон внутри графика

                # Рисуем новый график
                self.graph_widget.plot(x_vals, y_vals, pen=pg.mkPen(color='b', width=2), name=function_text)
                self.graph_widget.setXRange(self.left_border, self.right_border)
                self.graph_widget.setLabel('left', 'y')
                self.graph_widget.setLabel('bottom', 'x')
                self.graph_widget.setTitle(f"График функции: {function_text}", color='k')  # Черный цвет заголовка

                # # Добавляем вертикальные пунктирные линии на границах интервала
                # left_line = pg.InfiniteLine(pos=self.left_border, angle=90,
                #                             pen=pg.mkPen(color='r', width=1, style=pg.PenStyle.DashLine))
                # right_line = pg.InfiniteLine(pos=self.right_border, angle=90,
                #                              pen=pg.mkPen(color='r', width=1, style=pg.PenStyle.DashLine))

                # Устанавливаем границы, за которые нельзя выходить
                view_box = self.graph_widget.getViewBox()
                view_box.setLimits(
                    xMin=self.left_border,
                    xMax=self.right_border,
                    yMin=min(y_vals),
                    yMax=max(y_vals),
                )

        except Exception as e:
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")

        return True

    def calculate(self):
        try:
            if self.validate_fields():
                root_amount = root_counter(self.left_border, self.right_border, self.func)
                if root_amount > 1:
                    self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, содержащий только 1 корень.")
                    return
        except (TypeError, AttributeError):
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec()

    def show_hints(self):
        self.hint_window = HintWindow()
        self.hint_window.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())