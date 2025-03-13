import sympy as sp

def parse_function(func_str):
    x = sp.symbols('x')  # Объявляем переменную x
    try:
        func = sp.sympify(func_str)  # Преобразуем строку в выражение sympy
        return func
    except sp.SympifyError:
        print("Ошибка: некорректное математическое выражение")
        return None

# Пример использования:
func_expr = parse_function("sin(x) + 2*x + 1")
print(func_expr)  # Выведет: x**2 + 2*x + 1