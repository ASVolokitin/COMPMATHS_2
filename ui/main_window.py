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
        self.selected_value = None
        self.first_system_function_text = None
        self.first_system_function = None
        self.draw_graph_button = None
        self.x_left_border_input = None
        self.x_right_border_input = None
        self.y_left_border_input = None
        self.y_right_border_input = None
        self.first_system_function_input = None
        self.second_system_function_input = None
        self.second_system_function_text = None
        self.second_system_function = None
        self.single_function_text = None
        self.second_function_text = None
        self.single_function = None
        self.second_function = None
        self.x_left_border = -1
        self.x_right_border = 1
        self.y_left_border = -1
        self.y_right_border = 1
        self.x_input_layout = QHBoxLayout()
        self.accuracy = 0.05
        self.is_solving_system = False
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 500, 700)

        self.main_layout = QVBoxLayout()

        self.selected_option = None
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

        self.x_left_border_input = QLineEdit(self)
        self.x_right_border_input = QLineEdit(self)
        self.accuracy_input = QLineEdit(self)
        self.y_left_border_input = QLineEdit(self)
        self.y_right_border_input = QLineEdit(self)

        validator = QDoubleValidator()
        self.x_left_border_input.setValidator(validator)
        self.x_right_border_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)
        self.y_left_border_input.setValidator(validator)
        self.y_right_border_input.setValidator(validator)

        self.x_left_border_input.setPlaceholderText(f"Левый предел ({self.x_left_border})")
        self.x_right_border_input.setPlaceholderText(f"Правый предел ({self.x_right_border})")
        self.accuracy_input.setPlaceholderText(f"Точность ({self.accuracy})")
        self.y_left_border_input.setPlaceholderText(f"Левый предел для y ({self.y_left_border})")
        self.y_right_border_input.setPlaceholderText(f"Правый предел для y ({self.y_right_border})")

        self.x_input_layout.addWidget(self.x_left_border_input)
        self.x_input_layout.addWidget(self.x_right_border_input)
        self.x_input_layout.addWidget(self.accuracy_input)
        self.main_layout.addLayout(self.x_input_layout)

        y_input_layout = QHBoxLayout()
        y_input_layout.addWidget(self.y_left_border_input)
        y_input_layout.addWidget(self.y_right_border_input)
        self.main_layout.addLayout(y_input_layout)

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        # Кнопка для построения графика
        self.draw_graph_button = QPushButton("Построить", self)
        self.draw_graph_button.clicked.connect(self.draw_graph)
        button_layout.addWidget(self.draw_graph_button)

        # self.function_combo_box = FunctionSelectionComboBox(system_functions_options, self)
        # self.function_combo_box.function_selected.connect(self.on_function_selected)
        # self.main_layout.addWidget(self.function_combo_box)

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
        self.graph_widget.showGrid(x=True, y=True, alpha=0.5)
        self.graph_widget.getViewBox().setBackgroundColor('w')  # Белый фон внутри графика

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
        self.selected_value = key
        print(f"Вы выбрали: {self.selected_value}")

    def validate_single_fields(self):
        try:
            left_border = float(self.x_left_border_input.text().replace(",", ".")) if self.x_left_border_input.text() else self.x_left_border
            right_border = float(self.x_right_border_input.text().replace(",", ".")) if self.x_right_border_input.text() else self.x_right_border
            accuracy = float(self.accuracy_input.text().replace(",", ".")) if self.accuracy_input.text() else self.accuracy

            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого.")
                return False
            if right_border - left_border > MAX_INTERVAL_LENGTH:
                self.show_error("Ошибка диапазона", f"Выбран слишком широкий интервал (максимум = {MAX_INTERVAL_LENGTH}).")
                return False
            if right_border - left_border < MIN_INTERVAL_LENGTH:
                self.show_error(f"Ошибка диапазона", f"Выбран слишком узкий интервал (минимум = {MIN_INTERVAL_LENGTH}).")
                return False
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом.")
                return False

            self.x_left_border = left_border
            self.x_right_border = right_border
            self.accuracy = accuracy
            return True
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

    # def try_to_assign_first_function(self):
    #     function_text = self.single_function_input.text().strip().replace(",", ".")
    #     if "=" in function_text:
    #         self.show_error("Ошибка", "Задавайте уравнение функцией f(x), где f(x) = 0.")
    #         return False
    #     if not function_text:
    #         self.show_error("Ошибка", "Введите функцию")
    #         return False
    #     try:
    #         x_sym = sp.symbols('x')
    #         self.single_function = sp.lambdify(x_sym, parse_single_function(function_text, 'x'), 'numpy')
    #         self.single_function_text = function_text
    #         if self.single_function is None:
    #             self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
    #             return False
    #         return True
    #     except Exception as e:
    #         self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")
    #         return False

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
                    if self.first_system_function is None:
                        self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                        return False
                return True
            else:
                raise RuntimeError
        except (Exception, RuntimeError) as e:
            self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")


    def try_to_assign_second_function(self):
        function_text = self.second_system_function_input.text().strip().replace(",", ".")
        if "=" in function_text:
            self.show_error("Ошибка", "Задавайте уравнение функцией f(x), где f(x) = 0.")
            return False
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False
        try:
            y_sym = sp.symbols('x')
            self.second_function = sp.lambdify(y_sym, parse_single_function(function_text, 'x'), 'numpy')
            self.second_function_text = function_text
            if self.second_function is None:
                self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                return False
            return True
        except Exception as e:
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")
            return False

    # def validate_all(self):
    #     if self.validate_fields():
    #         if self.try_to_assign_first_function():
    #             if self.is_solving_system:
    #                 return self.try_to_assign_second_function()
    #             return True
    #         return False
    #     return False

    def validate_all(self):
        if not self.is_solving_system:
            return self.validate_single_fields() and self.try_to_assign_single_function()
        else:
            return self.try_to_assign_system()


    def draw_graph(self):
        if self.validate_all():
            x_vals = np.linspace(self.x_left_border, self.x_right_border, SAMPLES_AMOUNT)
            if not self.is_solving_system:
                try:
                    y_vals = self.single_function(x_vals)
                    self.graph_widget.clear()
                    self.graph_widget.plot(x_vals, y_vals, pen=pg.mkPen(color='b', width=2), name=self.single_function_text)
                    self.graph_widget.setXRange(self.x_left_border, self.x_right_border)
                    self.graph_widget.setLabel('left', 'y')
                    self.graph_widget.setLabel('bottom', 'x')
                    self.graph_widget.setTitle(f"График функции: {self.single_function_text}",
                                               color='k')  # Черный цвет заголовка

                    # Устанавливаем границы, за которые нельзя выходить
                    view_box = self.graph_widget.getViewBox()
                    view_box.setLimits(
                        xMin=self.x_left_border,
                        xMax=self.x_right_border,
                        yMin=min(y_vals),
                        yMax=max(y_vals),
                    )
                except (OverflowError) as e:
                    self.show_error("Ошибка вычисления",
                                    "Функция принимает слишком большие значения. Измените интервал.")
                    return
                # except (TypeError, NameError) as e:
                #     self.show_error("Ошибка ввода", "Некорректный формат формулы, воспользуйтесь подсказками")
            else:
                print(self.first_system_function(1, 1))
                print(self.second_system_function(1, 1))
                # try:

                # Здесь нужно графически изобразить систему, код ниже - не актуальный

                #     # Вычисляем значения для первой функции
                #     y_vals_first = self.first_system_function(x_vals)
                #
                #     # Вычисляем значения для второй функции
                #     y_vals_second = self.second_system_function(x_vals)
                #
                #     # Очищаем график
                #     self.graph_widget.clear()
                #
                #     # Отрисовываем первую функцию (синий цвет)
                #     self.graph_widget.plot(x_vals, y_vals_first, pen=pg.mkPen(color='b', width=2),
                #                            name=self.first_function_text)
                #
                #     # Отрисовываем вторую функцию (красный цвет)
                #     self.graph_widget.plot(x_vals, y_vals_second, pen=pg.mkPen(color='r', width=2),
                #                            name=self.second_function_text)
                #
                #     # Устанавливаем диапазон по оси X
                #     self.graph_widget.setXRange(self.x_left_border, self.x_right_border)
                #
                #     # Устанавливаем подписи осей
                #     self.graph_widget.setLabel('left', 'y')
                #     self.graph_widget.setLabel('bottom', 'x')
                #
                #     # Устанавливаем заголовок с именами обеих функций
                #     self.graph_widget.setTitle(
                #         f"Графики функций: {self.first_function_text} и {self.second_function_text}",
                #         color='k')  # Черный цвет заголовка
                #
                #     # Устанавливаем границы для оси Y, учитывая обе функции
                #     view_box = self.graph_widget.getViewBox()
                #     view_box.setLimits(
                #         xMin=self.x_left_border,
                #         xMax=self.x_right_border,
                #         yMin=min(min(y_vals_first), min(y_vals_second)),  # Минимум из двух функций
                #         yMax=max(max(y_vals_first), max(y_vals_second)),  # Максимум из двух функций
                #     )
                # except OverflowError as e:
                #     self.show_error("Ошибка вычисления",
                #                     "Функция принимает слишком большие значения. Измените интервал.")
                #     return
                # except (TypeError, NameError) as e:
                #     self.show_error("Ошибка ввода", "Некорректный формат формулы, воспользуйтесь подсказками")
        else:
            self.show_error("Ошибка", "Неверный формат функции.")
    def add_function(self):
        self.single_function_input.hide()
        self.add_function_button.hide()
        self.combo_box.show()
        self.remove_function_button.show()
        self.y_left_border_input.show()
        self.y_right_border_input.show()
        self.x_input_layout.removeWidget(self.accuracy_input)
        self.main_layout.insertWidget(self.main_layout.indexOf(self.x_input_layout) + 2, self.accuracy_input)
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
        self.is_solving_system = True

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
                        # self.update_result_table(self.calculate_one())
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