from PyQt6.QtWidgets import QVBoxLayout, QDialog, QTextEdit


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
            "Задавайте уравнения в виде функций f(x), таких что f(x) = 0.\n\n"
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