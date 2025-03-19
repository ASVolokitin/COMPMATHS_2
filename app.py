import sys
import numpy as np
import sympy as sp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QDialog, QTextEdit, QFileDialog
)
from PyQt6.QtGui import QDoubleValidator
import pyqtgraph as pg
from pyqtgraph import IsocurveItem

# Константы
MIN_INTERVAL_LENGTH = 0.5
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
        self.hint_text.setReadOnly(True)
        self.hint_text.setPlainText(
            "Задавайте уравнения в виде функций f(x, y), таких что f(x, y) = 0.\n\n"
            "Примеры ввода функций:\n\n"
            "1. Полиномы: x**2 + y**2 - 4\n"
            "2. Тригонометрические функции: sin(x) + cos(y)\n"
            "3. Экспоненты: exp(x) - y\n"
            "4. Логарифмы: log(x) + log(y)\n"
            "5. Комбинированные: x**2 + sin(y) - exp(x)\n\n"
            "Допустимые операторы: +, -, *, /, ** (степень)\n"
            "Допустимые функции: sin, cos, tan, exp, log, sqrt и др.\n"
            "Используйте 'x' и 'y' как переменные."
        )
        layout.addWidget(self.hint_text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.first_system_function_text = None
        self.first_system_function = None
        self.second_system_function_text = None
        self.second_system_function = None
        self.single_function_text = None
        self.single_function = None
        self.left_border = -1
        self.right_border = 1
        self.accuracy = 0.05
        self.is_solving_system = False
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 800, 800)

        self.main_layout = QVBoxLayout()

        # Поле для ввода функции
        self.single_function_input = QLineEdit(self)
        self.single_function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        self.main_layout.addWidget(self.single_function_input)

        self.first_system_function_input = QLineEdit(self)
        self.first_system_function_input.setPlaceholderText("Введите функцию, например: x**2 + y**2 - 4")
        self.main_layout.addWidget(self.first_system_function_input)
        self.first_system_function_input.hide()

        self.second_system_function_input = QLineEdit(self)
        self.second_system_function_input.setPlaceholderText("Введите функцию, например: sin(x) - y")
        self.main_layout.addWidget(self.second_system_function_input)
        self.second_system_function_input.hide()

        # Поля для ввода границ и точности
        self.left_border_input = QLineEdit(self)
        self.right_border_input = QLineEdit(self)
        self.accuracy_input = QLineEdit(self)

        validator = QDoubleValidator()
        self.left_border_input.setValidator(validator)
        self.right_border_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)

        self.left_border_input.setPlaceholderText(f"Левый предел ({self.left_border})")
        self.right_border_input.setPlaceholderText(f"Правый предел ({self.right_border})")
        self.accuracy_input.setPlaceholderText(f"Точность ({self.accuracy})")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.left_border_input)
        input_layout.addWidget(self.right_border_input)
        input_layout.addWidget(self.accuracy_input)
        self.main_layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        # Кнопка для построения графика
        self.draw_graph_button = QPushButton("Построить", self)
        self.draw_graph_button.clicked.connect(self.draw_graph)
        button_layout.addWidget(self.draw_graph_button)

        self.add_function_button = QPushButton("Добавить уравнение")
        self.add_function_button.clicked.connect(self.add_function)
        button_layout.addWidget(self.add_function_button)

        self.remove_function_button = QPushButton("Удалить второе уравнение")
        self.remove_function_button.clicked.connect(self.remove_function)
        button_layout.addWidget(self.remove_function_button)
        self.remove_function_button.hide()

        self.hints_button = QPushButton("Подсказки по вводу", self)
        button_layout.addWidget(self.hints_button)
        self.hints_button.clicked.connect(self.show_hints)

        # Виджет для отображения графика (PyQtGraph)
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')  # Белый фон
        self.main_layout.addWidget(self.graph_widget)
        self.graph_widget.getAxis('left').setPen(pg.mkPen(color='k'))  # Черный цвет для оси Y
        self.graph_widget.getAxis('bottom').setPen(pg.mkPen(color='k'))  # Черный цвет для оси X
        self.graph_widget.showGrid(x=True, y=True, alpha=0.5)

        # Кнопка для вычисления корней
        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        self.main_layout.addWidget(self.calc_button)

        # Таблица для отображения результатов
        self.result_table = QTableWidget(0, 4)
        self.result_table.setHorizontalHeaderLabels(["Метод", "Количество итераций", "Найденный корень", "Значение функции"])
        self.main_layout.addWidget(self.result_table)
        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setStretchLastSection(True)

        self.save_button = QPushButton("Сохранить результаты в файл", self)
        self.save_button.clicked.connect(self.save_results)
        self.main_layout.addWidget(self.save_button)
        self.save_button.hide()

        self.setLayout(self.main_layout)

    def validate_single_fields(self):
        try:
            left_border = float(self.left_border_input.text().replace(",", ".")) if self.left_border_input.text() else self.left_border
            right_border = float(self.right_border_input.text().replace(",", ".")) if self.right_border_input.text() else self.right_border
            accuracy = float(self.accuracy_input.text().replace(",", ".")) if self.accuracy_input.text() else self.accuracy

            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого.")
                return False
            if right_border - left_border > MAX_INTERVAL_LENGTH:
                self.show_error("Ошибка диапазона", f"Выбран слишком широкий интервал (максимум = {MAX_INTERVAL_LENGTH}).")
                return False
            if right_border - left_border < MIN_INTERVAL_LENGTH:
                self.show_error("Ошибка диапазона", f"Выбран слишком узкий интервал (минимум = {MIN_INTERVAL_LENGTH}).")
                return False
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом.")
                return False

            self.left_border = left_border
            self.right_border = right_border
            self.accuracy = accuracy
            return True
        except:
            self.show_error("Ошибка диапазона", "Некорректный ввод границ или точности.")
            return False

    def try_to_assign_single_function(self):
        function_text = self.single_function_input.text().strip().replace(",", ".")
        if "=" in function_text:
            self.show_error("Ошибка", "Задавайте уравнение функцией f(x), где f(x) = 0.")
            return False
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False
        try:
            self.single_function = sp.lambdify(sp.symbols('x'), parse_single_function(function_text, 'x'), 'numpy')
            self.single_function_text = function_text
            if self.single_function is None:
                self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                return False
            return True
        except Exception as e:
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")
            return False

    def try_to_assign_system(self):
        function_text = self.first_system_function_input.text().strip().replace(",", ".")
        if "=" in function_text:
            self.show_error("Ошибка", "Задавайте уравнение функцией f(x, y), где f(x, y) = 0.")
            return False
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False
        try:
            parsed_func = parse_multi_variable_function(function_text, ('x', 'y'))
            if parsed_func is not None:
                self.first_system_function = sp.lambdify(sp.symbols('x y'), parsed_func, 'numpy')
                self.first_system_function_text = function_text
                if self.first_system_function is None:
                    self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                    return False
                function_text = self.second_system_function_input.text().strip().replace(",", ".")
                if "=" in function_text:
                    self.show_error("Ошибка", "Задавайте уравнение функцией f(x, y), где f(x, y) = 0.")
                    return False
                if not function_text:
                    self.show_error("Ошибка", "Введите функцию")
                    return False
                parsed_func = parse_multi_variable_function(function_text, ('x', 'y'))
                if parsed_func is not None:
                    self.second_system_function = sp.lambdify(sp.symbols('x y'), parsed_func, 'numpy')
                    self.second_system_function_text = function_text
                    if self.second_system_function is None:
                        self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                        return False
                return True
            else:
                raise RuntimeError
        except (Exception, RuntimeError) as e:
            self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")

    def validate_all(self):
        if not self.is_solving_system:
            return self.validate_single_fields() and self.try_to_assign_single_function()
        else:
            return self.try_to_assign_system()

    def draw_graph(self):
        if self.validate_all():
            x = np.linspace(self.left_border, self.right_border, SAMPLES_AMOUNT)
            y = np.linspace(self.left_border, self.right_border, SAMPLES_AMOUNT)
            X, Y = np.meshgrid(x, y)

            self.graph_widget.clear()

            if not self.is_solving_system:
                try:
                    Z = self.single_function(X)
                    self.graph_widget.plot(x, Z, pen=pg.mkPen(color='b', width=2), name=self.single_function_text)
                except Exception as e:
                    self.show_error("Ошибка", "Ошибка при вычислении функции.")
            else:
                try:
                    Z1 = self.first_system_function(X, Y)
                    Z2 = self.second_system_function(X, Y)

                    # Отрисовка контурных линий для f(x, y) = 0
                    contour1 = pg.IsocurveItem(data=Z1, level=0, pen=pg.mkPen(color='b', width=2))
                    self.graph_widget.addItem(contour1)

                    # Отрисовка контурных линий для g(x, y) = 0
                    contour2 = pg.IsocurveItem(data=Z2, level=0, pen=pg.mkPen(color='r', width=2))
                    self.graph_widget.addItem(contour2)

                except Exception as e:
                    self.show_error("Ошибка", "Ошибка при вычислении системы функций.")

            self.graph_widget.setXRange(self.left_border, self.right_border)
            self.graph_widget.setYRange(self.left_border, self.right_border)
            self.graph_widget.setLabel('left', 'y')
            self.graph_widget.setLabel('bottom', 'x')
            self.graph_widget.setTitle(f"График функции: {self.single_function_text if not self.is_solving_system else 'Система уравнений'}")

    def add_function(self):
        self.single_function_input.hide()
        self.first_system_function_input.show()
        self.second_system_function_input.show()
        self.remove_function_button.show()
        self.add_function_button.hide()
        self.is_solving_system = True

    def remove_function(self):
        self.add_function_button.show()
        self.single_function_input.show()
        self.first_system_function_input.hide()
        self.second_system_function_input.hide()
        self.remove_function_button.hide()
        self.is_solving_system = False

    def calculate(self):
        if self.validate_all():
            self.draw_graph()
            if not self.is_solving_system:
                self.calculate_one()
            else:
                self.calculate_system()

    def calculate_one(self):
        results = []
        # Здесь добавьте вызовы методов для нахождения корней
        self.update_result_table(results)

    def calculate_system(self):
        results = []
        # Здесь добавьте вызовы методов для нахождения корней системы
        self.update_result_table(results)

    def update_result_table(self, results):
        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        self.result_table.setRowCount(len(results))

        for row, (method, data) in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(method))
            self.result_table.setItem(row, 1, QTableWidgetItem(str(data["iter_amount"]) if data["status_msg"] == "OK" else data["status_msg"]))
            self.result_table.setItem(row, 2, QTableWidgetItem("Не найден" if data['root'] is None else f"{data['root']:.15f}"))
            self.result_table.setItem(row, 3, QTableWidgetItem("Метод не применим" if data['value'] is None else f"{data['value']:.15f}"))
        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setStretchLastSection(True)

    def save_results(self):
        try:
            if self.result_table.rowCount() == 0:
                self.show_error("Ошибка", "Нет данных для сохранения.")
                return

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "Text Files (*.txt);;All Files (*)")

            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as file:
                headers = [self.result_table.horizontalHeaderItem(i).text() for i in range(self.result_table.columnCount())]
                file.write("\t".join(headers) + "\n")

                for row in range(self.result_table.rowCount()):
                    row_data = []
                    for col in range(self.result_table.columnCount()):
                        item = self.result_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    file.write("\t".join(row_data) + "\n")

            QMessageBox.information(self, "Успех", "Результаты успешно сохранены.")

        except PermissionError:
            self.show_error("Ошибка", "Нет доступа для записи в файл.")
        except Exception as e:
            self.show_error("Ошибка", f"Произошла ошибка при сохранении: {str(e)}")

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec()

    def show_hints(self):
        self.hint_window = HintWindow()
        self.hint_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())