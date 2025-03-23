import math

import numpy as np

class EquationSystem:
    def __init__(self, name, first_func, first_func_text, first_phi, first_phi_dx, first_phi_dy, second_func, second_func_text, second_phi, second_phi_dx, second_phi_dy):
        self.name = name
        self.first_func = first_func
        self.first_func_text = first_func_text
        self.first_phi = first_phi
        self.first_phi_dx = first_phi_dx
        self.first_phi_dy = first_phi_dy
        self.second_func = second_func
        self.second_func_text = second_func_text
        self.second_phi = second_phi
        self.second_phi_dx = second_phi_dx
        self.second_phi_dy = second_phi_dy

    def __repr__(self):
        return f"<{self.name}: [{self.first_func_text}], [{self.second_func_text}]>"

class System1(EquationSystem):
    def __init__(self):
        super().__init__(
            name="Система 1",
            first_func=lambda x, y: 3 * x + x ** 3 + (y - 1) ** 2 - 2,
            first_func_text="3 * x + x ** 3 + (y - 1) ** 2 - 2",
            first_phi=lambda x, y: -(x ** 3 + (y - 1) ** 2 - 2) / 3,
            first_phi_dx=lambda x, y: -x**2,
            first_phi_dy=lambda x, y: -2*(y + 1) / 3,
            second_func=lambda x, y: x**2 - 2 * y,
            second_func_text="x**2 - 2 * y",
            second_phi=lambda x, y: x**2 / 2,
            second_phi_dx=lambda x, y: x,
            second_phi_dy=lambda x, y: 0
        )

class System2(EquationSystem):
    def __init__(self):
        super().__init__(
            name="Система 2",
            first_func=lambda x, y: x - y**2 * np.sin(3 * y),
            first_func_text="бла бла",
            first_phi=lambda x, y: y**2 * np.sin(3 * y),
            first_phi_dx=0,
            first_phi_dy=0,
            second_func=lambda x, y: y - x**2,
            second_func_text="бла бла бла",
            second_phi=lambda x, y: x**2,
            second_phi_dx=0,
            second_phi_dy=0
        )

class System3(EquationSystem):
    def __init__(self):
        super().__init__(
            name="Система 3",
            first_func=lambda x, y: 2 * y - (x * 4)**3 + 30 * x,
            first_func_text="2 * y - (x * 4)**3 + 30 * x",
            first_phi=lambda x, y: math.cbrt(2 * y + 30 * x) / 4,
            first_phi_dx=lambda x, y: 5 / (2 * np.cbrt((2 * y + 30 * x)**2)),
            first_phi_dy=lambda x, y: 1 / (6 * np.cbrt((2 * y + 30 * x)**2)),
            second_func=lambda x, y: -x**2 + y**3 - 4 * x,
            second_func_text="-x**2 + y**3 - 4 * x",
            second_phi=lambda x, y: math.cbrt(4 * x + x**2),
            second_phi_dx=lambda x, y: (4 + 2 * x) / 3 * np.cbrt(4 * x + x**2)**2,
            second_phi_dy=lambda x, y: 0
        )