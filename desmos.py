import sys
import numpy as np
import sympy as sp
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                             QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QTextEdit,
                             QFileDialog)
from PyQt6.QtGui import QDoubleValidator, QColor
import pyqtgraph as pg

from calcs import parse_function, root_counter, half_division, newton

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
        self.first_function_text = None
        self.second_function_text = None
        self.first_function = None
        self.second_function = None
        self.left_border = -1
        self.right_border = 1
        self.accuracy = 0.05
        self.is_solving_system = False
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Поиск корней функции")
        self.setGeometry(100, 100, 600, 600)

        self.main_layout = QVBoxLayout()

        # Поле для ввода функции
        self.first_function_input = QLineEdit(self)
        self.first_function_input.setPlaceholderText("Введите функцию, например: x**3 - 4*x + 1")
        self.main_layout.addWidget(self.first_function_input)

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
        self.graph_widget.setBackground('w')  # Устанавливаем белый фон
        self.main_layout.addWidget(self.graph_widget)
        self.graph_widget.getAxis('left').setPen(pg.mkPen(color='k'))  # Черный цвет для оси Y
        self.graph_widget.getAxis('bottom').setPen(pg.mkPen(color='k'))  # Черный цвет для оси X
        self.graph_widget.getAxis('left').setTextPen(pg.mkPen(color='k'))  # Черный цвет для текста оси Y
        self.graph_widget.getAxis('bottom').setTextPen(pg.mkPen(color='k'))  # Черный цвет для текста оси X

        # Настраиваем сетку
        self.graph_widget.showGrid(x=True, y=True, alpha=0.5)
        self.graph_widget.getViewBox().setBackgroundColor('w')  # Белый фон внутри графика

        # Кнопка для вычисления корней
        self.calc_button = QPushButton("Вычислить", self)
        self.calc_button.clicked.connect(self.calculate)
        self.main_layout.addWidget(self.calc_button)

        # Таблица для отображения результатов
        self.result_table = QTableWidget(0, 2)
        self.result_table.setHorizontalHeaderLabels(["Метод", "Найденный корень"])
        self.main_layout.addWidget(self.result_table)
        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setStretchLastSection(True)

        self.save_button = QPushButton("Сохранить результаты в файл", self)
        self.save_button.clicked.connect(self.save_results)
        self.main_layout.addWidget(self.save_button)
        self.save_button.hide()

        self.setLayout(self.main_layout)

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

    def try_to_assign_first_function(self):
        function_text = self.first_function_input.text().strip()
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False
        try:
            x_sym = sp.symbols('x')
            self.first_function = sp.lambdify(x_sym, parse_function(function_text, 'x'), 'numpy')
            self.first_function_text = function_text
            if self.first_function is None:
                self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                return False
            return True
        except Exception as e:
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")
            return False

    def try_to_assign_second_function(self):
        function_text = self.second_function_input.text().strip()
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False
        try:
            y_sym = sp.symbols('x')
            self.second_function = sp.lambdify(y_sym, parse_function(function_text, 'x'), 'numpy')
            self.second_function_text = function_text
            if self.second_function is None:
                self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
                return False
            return True
        except Exception as e:
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")
            return False

    def validate_function(self):
        function_text = self.second_function_input.text().strip()
        if not function_text:
            self.show_error("Ошибка", "Введите функцию")
            return False

        f = parse_function(function_text)
        if f is None:
            self.show_error("Ошибка", "Не удалось распознать функцию, обратитесь к подсказкам по вводу.")
            return False

    def validate_all(self):
        if self.validate_fields():
            if self.try_to_assign_first_function():
                if self.is_solving_system:
                    return self.try_to_assign_second_function()
                return True
            return False
        return False


    def draw_graph(self):
        if self.validate_all():
            x_vals = np.linspace(self.left_border, self.right_border, SAMPLES_AMOUNT)
            if not self.is_solving_system:
                try:
                    y_vals = self.first_function(x_vals)
                    self.graph_widget.clear()
                    self.graph_widget.plot(x_vals, y_vals, pen=pg.mkPen(color='b', width=2),
                                           name=self.first_function_text)
                    self.graph_widget.setXRange(self.left_border, self.right_border)
                    self.graph_widget.setLabel('left', 'y')
                    self.graph_widget.setLabel('bottom', 'x')
                    self.graph_widget.setTitle(f"График функции: {self.first_function_text}",
                                               color='k')  # Черный цвет заголовка

                    # Устанавливаем границы, за которые нельзя выходить
                    view_box = self.graph_widget.getViewBox()
                    view_box.setLimits(
                        xMin=self.left_border,
                        xMax=self.right_border,
                        yMin=min(y_vals),
                        yMax=max(y_vals),
                    )
                except (OverflowError) as e:
                        self.show_error("Ошибка вычисления",
                                        "Функция принимает слишком большие значения. Измените интервал.")
                        return
                except (TypeError, NameError) as e:
                    self.show_error("Ошибка ввода", "Некорректный формат формулы, воспользуйтесь подсказками")


            else:
                if self.try_to_assign_second_function():
                    try:
                        # Вычисляем значения для первой функции
                        y_vals_first = self.first_function(x_vals)

                        # Вычисляем значения для второй функции
                        y_vals_second = self.second_function(x_vals)

                        # Очищаем график
                        self.graph_widget.clear()

                        # Отрисовываем первую функцию (синий цвет)
                        self.graph_widget.plot(x_vals, y_vals_first, pen=pg.mkPen(color='b', width=2),
                                               name=self.first_function_text)

                        # Отрисовываем вторую функцию (красный цвет)
                        self.graph_widget.plot(x_vals, y_vals_second, pen=pg.mkPen(color='r', width=2),
                                               name=self.second_function_text)

                        # Устанавливаем диапазон по оси X
                        self.graph_widget.setXRange(self.left_border, self.right_border)

                        # Устанавливаем подписи осей
                        self.graph_widget.setLabel('left', 'y')
                        self.graph_widget.setLabel('bottom', 'x')

                        # Устанавливаем заголовок с именами обеих функций
                        self.graph_widget.setTitle(
                            f"Графики функций: {self.first_function_text} и {self.second_function_text}",
                            color='k')  # Черный цвет заголовка

                        # Устанавливаем границы для оси Y, учитывая обе функции
                        view_box = self.graph_widget.getViewBox()
                        view_box.setLimits(
                            xMin=self.left_border,
                            xMax=self.right_border,
                            yMin=min(min(y_vals_first), min(y_vals_second)),  # Минимум из двух функций
                            yMax=max(max(y_vals_first), max(y_vals_second)),  # Максимум из двух функций
                        )
                    except OverflowError as e:
                        self.show_error("Ошибка вычисления",
                                        "Функция принимает слишком большие значения. Измените интервал.")
                        return
                    except (TypeError, NameError) as e:
                        self.show_error("Ошибка ввода", "Некорректный формат формулы, воспользуйтесь подсказками")

        else: print("Ошибка при парсинге аргументов.")

    def add_function(self):
        self.second_function_input = QLineEdit(self)
        self.second_function_input.setPlaceholderText("Введите функцию, например: sin(x) - x^2")
        self.main_layout.insertWidget(self.layout().indexOf(self.draw_graph_button) + 2, self.second_function_input)
        self.add_function_button.hide()
        self.remove_function_button.show()
        self.is_solving_system = True

    def remove_function(self):
        self.add_function_button.show()
        self.second_function_input.hide()
        self.remove_function_button.hide()
        self.second_function = None
        self.second_function_text = None
        self.is_solving_system = False
        self.draw_graph()

    def update_result_table(self, results):
        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        self.result_table.setRowCount(len(results))
        for row, (method, root) in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(method))
            self.result_table.setItem(row, 1, QTableWidgetItem(f"{root:.6f}"))
        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setStretchLastSection(True)

    def calculate(self):
        try:
            if self.validate_all():
                self.draw_graph()
                if not self.is_solving_system:
                    root_amount = root_counter(self.left_border, self.right_border, self.first_function)
                    if root_amount != 1:
                        self.show_error("Ошибка диапазона", "Для корректной работы необходимо выбрать интервал, содержащий только 1 корень.")
                        return False
                    else:
                        self.update_result_table(self.calculate_one())



        except (TypeError, AttributeError):
            self.show_error("Ошибка", "Ошибка: Функция введена некорректно, обратитесь к подсказкам по вводу функций.")

    def calculate_one(self):
        results = []
        results.append(("Метод половинного деления", half_division(self.left_border, self.right_border, self.accuracy, self.first_function)))
        results.append(("Метод Ньютона", newton(self.left_border, self.right_border, self.accuracy, self.first_function)))
        self.save_button.show()
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

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())