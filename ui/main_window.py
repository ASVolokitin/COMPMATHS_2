import numpy as np
import sympy as sp
from PyQt6.QtWidgets import (QWidget, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QDialog, QTextEdit,
                             QFileDialog, QComboBox)
from PyQt6.QtGui import QDoubleValidator
import pyqtgraph as pg

from solvers.half_devision_solver import half_division
from solvers.newton_solver import newton
from solvers.simple_iteration_solver import simple_iteration
from ui.hint_window import HintWindow
from ui.widgets.function_selector import FunctionSelectionComboBox
from ui.widgets.graph_widget import GraphWidget
from ui.widgets.result_table import ResultTable
from ui.widgets.system_combobox import SystemComboBox
from util import parse_single_function, parse_multi_variable_function, root_counter, MAX_INTERVAL_LENGTH, \
    MIN_INTERVAL_LENGTH, SAMPLES_AMOUNT, system_functions_options


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.system_functions_options = system_functions_options
        self.selected_value = system_functions_options[0]
        self.first_system_function_text = None
        self.first_system_function = None
        self.draw_graph_button = None
        self.x_left_border_input = QLineEdit(self)
        self.x_right_border_input = QLineEdit(self)
        self.y_left_border_input = QLineEdit(self)
        self.y_right_border_input = QLineEdit(self)
        self.accuracy_input = QLineEdit(self)
        self.first_system_function_input = None
        self.second_system_function_input = None
        self.second_system_function_text = None
        self.second_system_function = None
        self.single_function_text = None
        self.single_function = None
        self.x_left_border = -1
        self.x_right_border = 1
        self.y_left_border = -1
        self.y_right_border = 1
        self.x_input_layout = QHBoxLayout()
        self.y_input_layout = QHBoxLayout()
        self.accuracy = 0.05
        self.is_solving_system = False
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 500, 700)

        self.main_layout = QVBoxLayout()

        self.combo_box = SystemComboBox()
        self.combo_box.currentTextChanged.connect(self.update_system_combobox)
        self.main_layout.addWidget(self.combo_box)
        self.combo_box.hide()

        # Поле для ввода функции
        self.single_function_input = QLineEdit(self)
        self.single_function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        self.main_layout.addWidget(self.single_function_input)

        self.first_system_function_input = QLineEdit(self)
        self.first_system_function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*y + 1")
        self.main_layout.addWidget(self.first_system_function_input)
        self.first_system_function_input.hide()

        self.second_system_function_input = QLineEdit(self)
        self.second_system_function_input.setPlaceholderText("Введите функцию, например: sin(x) - y**2")
        self.main_layout.addWidget(self.second_system_function_input)
        self.second_system_function_input.hide()

        # self.x_left_border_input = QLineEdit(self)
        # self.x_right_border_input = QLineEdit(self)
        # self.y_left_border_input = QLineEdit(self)
        # self.y_right_border_input = QLineEdit(self)

        validator = QDoubleValidator()
        self.x_left_border_input.setValidator(validator)
        self.x_right_border_input.setValidator(validator)
        self.y_left_border_input.setValidator(validator)
        self.y_right_border_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)

        self.x_left_border_input.setPlaceholderText(f"Левый предел ({self.x_left_border})")
        self.x_right_border_input.setPlaceholderText(f"Правый предел ({self.x_right_border})")
        self.accuracy_input.setPlaceholderText(f"Точность ({self.accuracy})")
        self.y_left_border_input.setPlaceholderText(f"Левый предел для y ({self.y_left_border})")
        self.y_right_border_input.setPlaceholderText(f"Правый предел для y ({self.y_right_border})")

        self.x_input_layout.addWidget(self.x_left_border_input)
        self.x_input_layout.addWidget(self.x_right_border_input)
        self.x_input_layout.addWidget(self.accuracy_input)
        self.main_layout.addLayout(self.x_input_layout)

        self.y_input_layout.addWidget(self.y_left_border_input)
        self.y_input_layout.addWidget(self.y_right_border_input)
        self.main_layout.addLayout(self.y_input_layout)

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

        self.y_left_border_input.hide()
        self.y_right_border_input.hide()
        self.remove_function_button.hide()

        self.hints_button = QPushButton("Подсказки по вводу", self)
        button_layout.addWidget(self.hints_button)
        self.hints_button.clicked.connect(self.show_hints)

        # Виджет для отображения графика (PyQtGraph)
        self.graph_widget = GraphWidget()
        self.main_layout.addWidget(self.graph_widget)

        # Настраиваем сетку
        # self.graph_widget.showGrid(x=True, y=True, alpha=0.5)
        # self.graph_widget.getViewBox().setBackgroundColor('w')  # Белый фон внутри графика

        # Кнопка для вычисления корней
        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        self.main_layout.addWidget(self.calc_button)

        self.result_table = ResultTable()
        self.main_layout.addWidget(self.result_table)

        self.save_button = QPushButton("Сохранить результаты в файл", self)
        self.save_button.clicked.connect(self.save_results)
        self.main_layout.addWidget(self.save_button)
        self.save_button.hide()

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
        if self.validate_borders(self.x_left_border_input, self.x_right_border_input):
            self.x_left_border = float(self.x_left_border_input.text().replace(",", "."))
            self.x_right_border = float(self.x_right_border_input.text().replace(",", "."))
            return True
        return False

    def validate_y_borders(self):
        if self.validate_borders(self.y_left_border_input, self.y_right_border_input):
            self.y_left_border = float(self.y_left_border_input.text().replace(",", "."))
            self.y_right_border = float(self.y_right_border_input.text().replace(",", "."))
            return True
        return False

    def validate_borders(self, left_border_field, right_border_field):
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

    def validate_all(self):
        if self.validate_x_borders() and self.validate_accuracy():
            print(f"Установлена левая граница X: {self.x_left_border}")
            print(f"Установлена правая граница X: {self.x_right_border}")
            print(f"Установлена точность: {self.accuracy}")
            if not self.is_solving_system:
                return self.try_to_assign_single_function()
            else:
                if self.validate_y_borders():
                    print(f"Установлена левая граница Y: {self.y_left_border}")
                    print(f"Установлена правая граница Y: {self.y_right_border}")
                    self.first_system_function = self.selected_value.first_func
                    self.second_system_function = self.selected_value.second_func
                    print("Значение: ", self.second_system_function(3, 3))
                    return True
                else:
                    return False
        else:
            return False

    def draw_graph(self):
        if self.validate_all():
            if not self.is_solving_system:
                self.graph_widget.plot_function(self.single_function, [self.x_left_border, self.x_right_border])
            else:
                self.graph_widget.plot_implicit_functions(self.first_system_function, self.second_system_function, [self.x_left_border, self.x_right_border], [self.y_left_border, self.y_right_border])

    def add_function(self):
        self.single_function_input.hide()
        self.add_function_button.hide()
        self.combo_box.show()
        self.remove_function_button.show()
        self.y_left_border_input.show()
        self.y_right_border_input.show()
        self.x_input_layout.removeWidget(self.accuracy_input)
        self.main_layout.insertWidget(self.main_layout.indexOf(self.y_input_layout) + 1, self.accuracy_input)
        self.is_solving_system = True

    def remove_function(self):
        self.single_function_input.show()
        self.add_function_button.show()
        self.combo_box.hide()
        self.remove_function_button.hide()
        self.y_left_border_input.hide()
        self.y_right_border_input.hide()
        self.main_layout.removeWidget(self.accuracy_input)
        self.x_input_layout.insertWidget(self.x_input_layout.indexOf(self.x_right_border_input) + 1, self.accuracy_input)
        self.is_solving_system = False

    def calculate(self):
        # try:
            if self.validate_all():
                self.draw_graph()
                if not self.is_solving_system:
                    root_amount = root_counter(self.x_left_border, self.x_right_border, self.single_function)
                    if root_amount != 1:
                        self.result_table.clearContents()
                        self.result_table.setRowCount(0)
                        self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, содержащий ровно 1 корень.")
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
        results.append(("Метод Ньютона", newton(self.x_left_border, self.x_right_border, self.accuracy, self.single_function)))
        results.append(("Метод простой итерации", simple_iteration(self.x_left_border, self.x_right_border, self.accuracy, self.single_function)))
        self.save_button.show()
        self.result_table.update_result_table_solo(results)
        return results

    def calculate_system(self):
        results = []
        self.save_button.show()
        self.result_table.update_result_table_solo(results)
        return results

    def save_results(self):
        try:
            if self.result_table.rowCount() == 0:
                self.show_error("Ошибка", "Нет данных для сохранения.")
                return

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "Text Files (*.txt);;All Files (*)")

            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as file:
                headers = [self.result_table.horizontalHeaderItem(i).text() for i in
                           range(self.result_table.columnCount())]
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