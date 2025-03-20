from PyQt6.QtWidgets import QComboBox

from entites.equation_system import System1
from util import system_functions_options # Импортируем словарь

class SystemComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = system_functions_options
        for system in self.data: self.addItem(system.name)
        # print(self.data[0].name)
          # Добавляем ключи словаря
        # self.currentTextChanged.connect(self.on_selection_change)

    # def on_selection_change(self, key):
    #     self.selected_key = key
    #     print(f"Выбрано: {self.selected_key}")