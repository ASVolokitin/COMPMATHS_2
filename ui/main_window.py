import csv
import math

import sympy as sp
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QCheckBox, QSizePolicy)
from PyQt6.QtGui import QDoubleValidator

from entites.json_parser import json_parser
from solvers.half_devision_solver import half_division
from solvers.newton_solver import newton
from solvers.simple_iteration_solver import simple_iteration
from solvers.system_simple_iteration_solver import system_simple_iteration_solver
from ui.hint_window import HintWindow
from ui.widgets.graph_widget import GraphWidget
from ui.widgets.result_table import ResultTable
from ui.widgets.system_combobox import SystemComboBox
from utils.calcs_util import root_counter, MAX_INTERVAL_LENGTH, MIN_INTERVAL_LENGTH, system_functions_options, \
    RootCounterErrorCode
from utils.ui_util import load_stylesheet


class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.system_functions_options = system_functions_options
        self.selected_value = system_functions_options[0]
        self.first_system_function_text = None
        self.first_system_function = None
        self.second_system_function = None
        self.single_function_input = QLineEdit(self)
        self.x_left_border_input = QLineEdit(self)
        self.x_right_border_input = QLineEdit(self)
        self.x_start_input = QLineEdit(self)
        self.y_bottom_border_input = QLineEdit(self)
        self.y_top_border_input = QLineEdit(self)
        self.y_start_input = QLineEdit(self)
        self.accuracy_input = QLineEdit(self)
        self.x_start = None
        self.y_start = None
        self.draw_graph_button = QPushButton("Построить")
        self.solve_system_button = QPushButton("Решить систему")
        self.solve_equation_button = QPushButton("Решить уравнение")
        self.load_file_button = QPushButton("Загрузить из файла")
        self.hints_button = QPushButton("Подсказки по вводу", self)
        self.single_function_text = None
        self.single_function = None
        self.x_left_border = -1
        self.x_right_border = 1
        self.y_bottom_border = -1
        self.y_top_border = 1
        self.x_input_layout = QHBoxLayout()
        self.y_input_layout = QHBoxLayout()
        self.accuracy = 0.05
        self.is_solving_system = False
        self.dev_mode = False
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Добро пожаловать в программу Никиты Копытова")
        self.setGeometry(0, 0, 760, 800)

        self.main_layout = QVBoxLayout()

        self.combo_box = SystemComboBox()
        self.combo_box.currentTextChanged.connect(self.update_system_combobox)
        self.main_layout.addWidget(self.combo_box)
        self.combo_box.hide()

        self.single_function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        self.main_layout.addWidget(self.single_function_input)

        validator = QDoubleValidator()
        self.x_left_border_input.setValidator(validator)
        self.x_right_border_input.setValidator(validator)
        self.x_start_input.setValidator(validator)
        self.y_bottom_border_input.setValidator(validator)
        self.y_top_border_input.setValidator(validator)
        self.y_start_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)

        self.x_left_border_input.setPlaceholderText(f"Левый предел по X")
        self.x_right_border_input.setPlaceholderText(f"Правый предел по X")
        self.x_start_input.setPlaceholderText("Начальное приближение по X")
        self.accuracy_input.setPlaceholderText(f"Точность (default = {self.accuracy})")
        self.y_bottom_border_input.setPlaceholderText(f"Нижний предел по Y")
        self.y_top_border_input.setPlaceholderText(f"Верхний предел по Y")
        self.y_start_input.setPlaceholderText("Начальное приближение по Y")

        self.x_input_layout.addWidget(self.x_left_border_input)
        self.x_input_layout.addWidget(self.x_right_border_input)
        self.x_input_layout.addWidget(self.x_start_input)
        self.x_input_layout.addWidget(self.accuracy_input)
        self.main_layout.addLayout(self.x_input_layout)

        self.y_input_layout.addWidget(self.y_bottom_border_input)
        self.y_input_layout.addWidget(self.y_top_border_input)
        self.y_input_layout.addWidget(self.y_start_input)
        self.main_layout.addLayout(self.y_input_layout)

        self.x_start_input.hide()
        self.y_start_input.hide()

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        self.draw_graph_button.clicked.connect(self.draw_graph)
        button_layout.addWidget(self.draw_graph_button)

        self.solve_equation_button.clicked.connect(self.remove_function)
        button_layout.addWidget(self.solve_equation_button)

        self.solve_system_button.clicked.connect(self.add_function)
        button_layout.addWidget(self.solve_system_button)

        self.y_bottom_border_input.hide()
        self.y_top_border_input.hide()
        self.solve_equation_button.hide()

        button_layout.addWidget(self.load_file_button)
        self.load_file_button.clicked.connect(self.load_file)

        button_layout.addWidget(self.hints_button)
        self.hints_button.clicked.connect(self.show_hints)

        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        self.main_layout.addWidget(self.calc_button)

        graph_layout = QHBoxLayout()
        self.graph_widget = GraphWidget()
        graph_layout.addWidget(self.graph_widget)
        graph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(graph_layout)

        self.result_table = ResultTable()
        self.result_table.setMaximumHeight(140)
        self.result_table.setDisabled(True)
        self.result_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.result_table, stretch=0)

        self.save_button = QPushButton("Сохранить результаты в файл", self)
        self.save_button.clicked.connect(self.save_results)
        self.main_layout.addWidget(self.save_button)
        self.save_button.hide()

        self.switch = QCheckBox("Режим разработчика")
        self.main_layout.addWidget(self.switch)
        self.switch.toggled.connect(self.toggle_dev_mode)
        self.setLayout(self.main_layout)

    def update_system_combobox(self, key):
        self.selected_value = self.combo_box.currentData()
        print(f"Вы выбрали: {self.selected_value} ({type(self.selected_value)})")


    def validate_accuracy(self):
        try:
            accuracy = float(
                self.accuracy_input.text().replace(",", ".")) if self.accuracy_input.text() else self.accuracy
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом.")
                return False

            self.accuracy = accuracy
            return True
        except ValueError:
            self.show_error("Ошибка точности", "Точность должна быть задана положительным числом")

    def validate_x_borders(self):
        if self.validate_border(self.x_left_border_input, self.x_right_border_input):
            self.x_left_border = float(self.x_left_border_input.text().replace(",", "."))
            self.x_right_border = float(self.x_right_border_input.text().replace(",", "."))
            return True
        return False

    def validate_y_borders(self):
        if self.validate_border(self.y_bottom_border_input, self.y_top_border_input):
            self.y_bottom_border = float(self.y_bottom_border_input.text().replace(",", "."))
            self.y_top_border = float(self.y_top_border_input.text().replace(",", "."))
            return True
        return False

    def validate_border(self, left_border_field, right_border_field):
        try:
            if left_border_field == "" or right_border_field == "":
                raise ValueError
            left_border = float(left_border_field.text().replace(",", "."))
            right_border = float(right_border_field.text().replace(",", "."))
            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого.")
                return False
            if right_border - left_border > MAX_INTERVAL_LENGTH:
                self.show_error("Ошибка диапазона", f"Выбран слишком широкий интервал (максимум = {MAX_INTERVAL_LENGTH}).")
                return False
            if right_border - left_border < MIN_INTERVAL_LENGTH:
                self.show_error(f"Ошибка диапазона", f"Выбран слишком узкий интервал (минимум = {MIN_INTERVAL_LENGTH}).")
                return False

            return True
        except ValueError:
            self.show_error("Ошибка диапазона", "Значения границ интервалов необходимо задавать числами.")
            return False
        except:
            self.show_error("Ошибка диапазона", "Балду какую-то вводишь братик")
            return False

    def validate_start_point(self):
        try:
            x_start = float(self.x_start_input.text().replace(",", "."))
            y_start = float(self.y_start_input.text().replace(",", "."))
            if not self.x_left_border <= x_start <= self.x_right_border:
                self.show_error("Ошибка выбора начального приближения", f"Начальное приближение по X должно быть между {self.x_left_border} и {self.x_right_border}.")
                return False
            if not self.y_bottom_border <= y_start <= self.y_top_border:
                self.show_error("Ошибка выбора начального приближения", f"Начальное приближение по X должно быть между {self.y_bottom_border} и {self.y_top_border}.")
                return False

            self.x_start = x_start
            self.y_start = y_start
            return True
        except ValueError:
            self.show_error("Ошибка начального приближения", "Начальное приближение необходимо задавать числами.")
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
            expr = sp.sympify(function_text)
            variables = expr.free_symbols
            if not variables.issubset({sp.Symbol('x')}):
                self.show_error("Ошибка", "Функция должна содержать только переменную x.")
                return False
            if str(expr) == "zoo":
                self.show_error("Ошибка", "Введённое выражение является неопределённостью")
                return False
            self.single_function = sp.lambdify(sp.symbols('x'), expr, 'numpy')
            self.single_function_text = function_text
            try:
                self.single_function(math.pi)
            except ZeroDivisionError:
                self.show_error("Функция не определена на всём интервале, рассмотрите другой.")
            if self.single_function is None:
                self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                return False
            return True
        except (sp.SympifyError, NameError, AttributeError) as e:
            self.show_error("Ошибка", "Ошибка: Синтаксис функции не соответствует формату, обратитесь к подсказкам по вводу.")
            return False

    def validate_borders(self):
        if self.validate_x_borders() and self.validate_accuracy():
            print(f"Установлена левая граница X: {self.x_left_border}")
            print(f"Установлена правая граница X: {self.x_right_border}")
            print(f"Установлена точность: {self.accuracy}")

            if self.is_solving_system:
                if self.validate_y_borders():
                    print(f"Установлена левая граница Y: {self.y_bottom_border}")
                    print(f"Установлена правая граница Y: {self.y_top_border}")
                    return True
                else:
                    return False
            return True
        else:
            return False

    def validate_all(self):
        if self.validate_borders():
            if self.is_solving_system:
                self.first_system_function = self.selected_value.first_func
                self.second_system_function = self.selected_value.second_func
                return self.validate_start_point()
            else:
                return self.try_to_assign_single_function()
        else:
            return False

    def validate_graph(self):
        if self.validate_borders():
            if self.is_solving_system:
                self.first_system_function = self.selected_value.first_func
                self.second_system_function = self.selected_value.second_func
                return True
            else:
                return self.try_to_assign_single_function()
        else:
            return False

    def draw_graph(self):
        # try:
            if self.validate_graph():
                if self.is_solving_system:
                    self.graph_widget.plot_implicit_functions(self.selected_value,
                                                              [self.x_left_border, self.x_right_border],
                                                              [self.y_bottom_border, self.y_top_border],
                                                              [self.x_start, self.y_start])
                else:
                    self.graph_widget.plot_function(self.single_function, self.single_function_text, [self.x_left_border, self.x_right_border])


    def add_function(self):
        self.single_function_input.hide()
        self.solve_system_button.hide()
        self.hints_button.hide()
        self.combo_box.show()
        self.solve_equation_button.show()
        self.y_bottom_border_input.show()
        self.y_top_border_input.show()
        self.x_start_input.show()
        self.y_start_input.show()
        self.x_input_layout.removeWidget(self.accuracy_input)
        self.main_layout.insertWidget(self.main_layout.indexOf(self.y_input_layout) + 1, self.accuracy_input)
        self.is_solving_system = True
        self.result_table.clear_table()

    def remove_function(self):
        self.single_function_input.show()
        self.solve_system_button.show()
        self.hints_button.show()
        self.combo_box.hide()
        self.solve_equation_button.hide()
        self.y_bottom_border_input.hide()
        self.y_top_border_input.hide()
        self.x_start_input.hide()
        self.y_start_input.hide()
        self.main_layout.removeWidget(self.accuracy_input)
        self.x_input_layout.insertWidget(self.x_input_layout.indexOf(self.x_right_border_input) + 1, self.accuracy_input)
        self.is_solving_system = False
        self.result_table.clear_table()

    def calculate(self):
        # try:
            if self.validate_all():
                self.draw_graph()
                if not self.is_solving_system:
                    root_amount = root_counter(self.x_left_border, self.x_right_border, self.single_function)
                    if root_amount != 1:
                        self.result_table.clearContents()
                        self.result_table.setRowCount(0)
                        if root_amount == RootCounterErrorCode.MORE_THAN_ONE_ROOT or root_amount == RootCounterErrorCode.NO_ROOTS:
                            self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, где функция пересекает OX единожды.")
                        elif root_amount == RootCounterErrorCode.DISCONTINUED_FUNCTION:
                            self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, где функция везде дифференцируема, выбранная функция терпит неустранивый разрыв.")
                        return False
                    else:
                        self.calculate_one()
                else:
                    self.calculate_system()
        # except (AttributeError, TypeError, NameError) as e:
        #     self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")

    def calculate_one(self):
        results = []
        results.append(("Метод половинного деления", half_division(self.x_left_border, self.x_right_border, self.accuracy, self.single_function)))
        # print("раз")
        results.append(("Метод Ньютона", newton(self.x_left_border, self.x_right_border, self.accuracy, self.single_function, self.dev_mode)))
        # print("два")
        results.append(("Метод простой итерации", simple_iteration(self.x_left_border, self.x_right_border, self.accuracy, self.single_function, self.dev_mode)))
        # print("три")
        for method_name, result in results:
            if result["status_msg"] == "OK":
                self.graph_widget.add_solution_point(result["root"], result["value"])

        self.save_button.show()
        self.result_table.update_result_table_solo(results)
        return results

    def calculate_system(self):
        results = []
        results.append(("Метод простой итерации", system_simple_iteration_solver(self.x_left_border, self.x_right_border, self.y_bottom_border, self.y_top_border, self.x_start, self.y_start, self.accuracy, self.selected_value, self.dev_mode)))
        print(results)
        for method_name, result in results:
            if result["status_msg"] == "OK":
                self.graph_widget.add_solution_point(result["root"], result["value"])
        print(result["status_msg"])
        self.save_button.show()
        self.result_table.update_result_table_system(results)
        return results

    def save_results(self):
        try:
            if self.result_table.rowCount() == 0:
                self.show_error("Ошибка", "Нет данных для сохранения.")
                return False

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить результаты",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )

            if not file_path: return False

            if not file_path.lower().endswith('.csv'): file_path += '.csv'

            data_rows = []
            headers = [self.result_table.horizontalHeaderItem(i).text()
                       for i in range(self.result_table.columnCount())]

            for row in range(self.result_table.rowCount()):
                row_data = []
                for col in range(self.result_table.columnCount()):
                    item = self.result_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data_rows.append(row_data)

            metadata = [
                f"# Функция: {self.single_function_text}" if not self.is_solving_system
                else f"# Первое уравнение системы: {self.selected_value.first_func_text}\n # Второе уравнение системы: {self.selected_value.second_func_text}",
                f"# Интервал по X: [{self.x_left_border}, {self.x_right_border}]",
                f"# Точность: {self.accuracy}"
            ]

            if self.is_solving_system:
                metadata.extend([
                    f"# Интервал по Y: [{self.y_bottom_border}, {self.y_top_border}]",
                    f"# Начальное приближение: ({self.x_start}, {self.y_start})"
                ])

            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                for line in metadata:
                    csvfile.write(line + '\n')

                writer = csv.writer(csvfile, delimiter=';', quotechar='"',quoting=csv.QUOTE_MINIMAL)

                writer.writerow(headers)
                writer.writerows(data_rows)
            QMessageBox.information(self, "Успех", "Результаты успешно сохранены в CSV файл.")
            return True

        except PermissionError:
            self.show_error("Ошибка", "Нет прав для записи в указанный файл.")
            return False
        except Exception as e:
            self.show_error("Ошибка", f"Произошла ошибка при сохранении CSV:\n{str(e)}")
            return False

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec()

    def show_hints(self):
        self.hint_window = HintWindow()
        self.hint_window.exec()

    def toggle_dev_mode(self):
        if self.dev_mode:
            self.app.setStyleSheet(load_stylesheet("style/light_mode.css"))
        else:
            self.app.setStyleSheet(load_stylesheet("style/dark_mode.css"))
        self.dev_mode = not self.dev_mode


    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                   "JSON файлы (*.json);;Текстовые файлы (*.txt);;Все файлы (*)")

        if file_name:
            try:
                if file_name.endswith(".json"):
                    data = json_parser.read_json(file_name)
                    print(f"Статус: Загружен JSON-файл. Данные: {data}")
                    if not self.is_solving_system:
                        parsed_data = json_parser.parse_equation(data)
                        self.x_left_border_input.setText(str(parsed_data["x_left_border"]))
                        self.x_right_border_input.setText(str(parsed_data["x_right_border"]))
                        self.accuracy_input.setText(str(parsed_data["accuracy"]))
                    else:
                        parsed_data = json_parser.parse_system(data)
                        self.x_left_border_input.setText(str(parsed_data["x_left_border"]))
                        self.x_right_border_input.setText(str(parsed_data["x_right_border"]))
                        self.y_bottom_border_input.setText(str(parsed_data["y_bottom_border"]))
                        self.y_top_border_input.setText(str(parsed_data["y_top_border"]))
                        self.x_start_input.setText(str(parsed_data["x_start"]))
                        self.y_start_input.setText(str(parsed_data["y_start"]))
                else:
                    self.show_error("Ошибка", "Неподдерживаемый формат файла.")
            except ValueError as e:
                self.show_error("Ошибка", str(e))
