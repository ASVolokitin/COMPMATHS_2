# TODO
# Добавить адаптивный дизайн
# Добавить Decimal
# Добавить проверки достаточных условий

import sys
from PyQt6.QtWidgets import (QApplication)
from ui.main_window import MainWindow
from util import load_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("style/style.css"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())