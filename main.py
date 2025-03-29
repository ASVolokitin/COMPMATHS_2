import sys
from PyQt6.QtWidgets import (QApplication)
from ui.main_window import MainWindow
from utils.ui_util import load_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("style/light_mode.css"))
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())