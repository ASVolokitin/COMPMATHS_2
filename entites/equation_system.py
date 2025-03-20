import numpy as np

class EquationSystem:
    def __init__(self, name, first_func, first_func_text, second_func, second_func_text):
        self.name = name
        self.first_func = first_func
        self.first_func_text = first_func_text
        self.second_func = second_func
        self.second_func_text = second_func_text

    def __repr__(self):
        return f"<{self.name}: [{self.first_func_text}], [{self.second_func_text}]>"

class System1(EquationSystem):
    def __init__(self):
        super().__init__(
            name="Система 1",
            first_func=lambda x, y: x**2 - 2 * y,
            first_func_text="x**2 - 2 * y",
            second_func=lambda x, y: np.sin(x * y) - 3 * x,
            second_func_text="sin(x * y) - 3 * x"
        )

class System2(EquationSystem):
    def __init__(self):
        super().__init__(
            name="Система 2",
            first_func=lambda x, y: np.exp(x**3) - 4 * x * y + 2 * y**2,
            first_func_text="exp(x**3) - 4 * x * y + 2 * y**2",
            second_func=lambda x, y: x**2 + y**2 - 3 * x * y - 7,
            second_func_text="x**2 + y**2 - 3 * x * y - 7"
        )