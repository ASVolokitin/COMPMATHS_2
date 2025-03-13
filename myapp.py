import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtGui import QDoubleValidator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Нахождение нуля функции")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        self.left_border = -1
        self.right_border = 1
        self.accuracy = 0.05
        self.left_border_label = QLabel(f"   = {self.left_border}", self)
        self.right_border_label = QLabel(f"right_border = {self.right_border}", self)
        self.accuracy_label = QLabel(f"accuracy = {self.accuracy}", self)

        self.left_border_label.move(20, 20)
        self.right_border_label.move(80, 20)
        self.accuracy_label.move(120, 20)

        self.left_border_input = QLineEdit(self)
        self.left_border_input.move(50, 50)
        self.right_border_input = QLineEdit(self)
        self.right_border_input.move(50, 100)
        self.accuracy_input = QLineEdit(self)
        self.accuracy_input.move(50, 150)

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.left_border_input.setValidator(validator)
        self.right_border_input.setValidator(validator)
        self.accuracy_input.setValidator(validator)

        calc_button = QPushButton("Вычислить", self)
        calc_button.move(50, 200)
        calc_button.clicked.connect(self.calculate)

    def calculate(self):

        left_border = self.left_border
        right_border = self.right_border
        accuracy = self.accuracy

        if self.left_border_input.text() != "": left_border = self.left_border_input.text().replace(",", ".")
        if self.right_border_input.text() != "": right_border = self.right_border_input.text().replace(",", ".")
        if self.accuracy_input.text() != "": accuracy = self.accuracy_input.text().replace(",", ".")

        try:
            left_border = float(left_border)
            right_border = float(right_border)
            accuracy = float(accuracy)

            if left_border >= right_border:
                self.show_error("Ошибка диапазона", "Левый предел должен быть меньше правого!")
                return
            if accuracy <= 0:
                self.show_error("Ошибка точности", "Точность должна быть положительным числом!")
                return

            self.left_border = left_border
            self.right_border = right_border
            self.accuracy = accuracy

            self.left_border_label.setText(f"a = {self.left_border}")
            self.right_border_label.setText(f"b = {self.right_border}")
            self.accuracy_label.setText(f"e = {self.accuracy}")

            self.left_border_label.adjustSize()
            self.right_border_label.adjustSize()
            self.accuracy_label.adjustSize()

            print(f"Левый предел: {self.left_border}, Правый предел: {self.right_border}, Точность: {self.accuracy}")

        except ValueError:
            self.show_error("Ошибка ввода", "Введите корректные числовые значения!")

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec()



app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())