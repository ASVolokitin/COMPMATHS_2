from PyQt6.QtWidgets import QComboBox

from utils.calcs_util import system_functions_options # Импортируем словарь

class SystemComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = system_functions_options
        for system in self.data: self.addItem(system.name, system)