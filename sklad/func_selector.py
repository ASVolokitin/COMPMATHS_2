from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal

class FunctionSelectionComboBox(QComboBox):
    function_selected = pyqtSignal(dict)
    def __init__(self, options_dict, parent=None):
        super().__init__(parent)
        self.options_dict = options_dict
        self.populate_combo_box()
        self.currentIndexChanged.connect(self.on_selection_change)

    def populate_combo_box(self):
        self.clear()
        for key in self.options_dict.keys():
            self.addItem(key)

    def on_selection_change(self, index):
        selected_key = self.currentText()
        selected_functions = self.options_dict.get(selected_key)
        if selected_functions:
            self.function_selected.emit(selected_functions)