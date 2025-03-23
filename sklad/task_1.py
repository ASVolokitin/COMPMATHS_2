import math
import numpy as np

from archive import derivative


def chord_method(f, a, b, tol=1e-2, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала [a, b].")

    iter_count = 0
    prev_x = a
    while iter_count < max_iter:
        # Вычисляем точку пересечения хорды с осью x
        x = a - f(a) * (b - a) / (f(b) - f(a))

        # Проверяем условие сходимости
        if abs(f(x)) < tol:
            print(abs(x - prev_x))
            print(f"Шаг {iter_count + 1}: a = {round(a, 3)}, b = {round(b, 3)}, x = {round(x, 3)}, f(a) = {round(f(a), 3)}, f(b) = {round(f(b), 3)}, f(x) = {round(f(x), 3)}, xk - xk-1 = {round(x - prev_x, 3)}")

            print(f"Корень найден за {iter_count} итераций.")
            return x

        print(
            f"Шаг {iter_count + 1}: a = {round(a, 3)}, b = {round(b, 3)}, x = {round(x, 3)}, f(a) = {round(f(a), 3)}, f(b) = {round(f(b), 3)}, f(x) = {round(f(x), 3)}, xk - xk-1 = {round(x - prev_x, 3)}")
        # Обновляем границы интервала
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        prev_x = x
        iter_count += 1

    print(f"Достигнуто максимальное количество итераций ({max_iter}).")
    return x

def simple_iteration_method(g, x0, tol=1e-2, max_iter=100):
    # fun = lambda x: -2.7 * x ** 3 - 1.48 * x ** 2 + 19.23 * x + 6.35
    """
    Находит корень уравнения x = first_func(x) методом простой итерации.

    Параметры:
    first_func: функция, задающая итерационный процесс.
    x0: начальное приближение.
    tol: допустимая погрешность (точность).
    max_iter: максимальное количество итераций.

    Возвращает:
    x: приближенное значение корня.
    """
    iter_count = 0
    x = x0
    while iter_count < max_iter:
        x_new = g(x)  # Вычисляем новое значение
        print(f"{iter_count + 1}: {round(x, 3)} {round(x_new, 3)} {round(g(x_new), 3)} {round(abs(x_new - x), 3)}")

        # Проверяем условие сходимости
        if abs(x_new - x) < tol:
            print(f"Корень найден за {iter_count} итераций.")
            return x_new

        # Обновляем значение x
        x = x_new
        iter_count += 1

    print(f"Достигнуто максимальное количество итераций ({max_iter}).")
    return x


def g(x):
    return math.cbrt((-1.48 * x**2 + 19.23 * x + 6.35)/2.7)

# Начальное приближение
x0 = -2.5

# Находим корень
# root = simple_iteration_method(first_func, x0)
# print(f"Найденный корень: {root:.6f}")

fun = lambda x : -2.7 * x**3 - 1.48 * x**2 + 19.23 * x + 6.35
# print(derivative(first_func, -3))
# print(derivative(first_func, -2))

# chord_method(fun, 2, 3)

def secant_method(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Находит корень уравнения f(x) = 0 методом секущих.

    Параметры:
    f: функция, корень которой нужно найти.
    x0, x1: начальные приближения.
    tol: допустимая погрешность (точность).
    max_iter: максимальное количество итераций.

    Возвращает:
    x: приближенное значение корня.
    """
    iter_count = 0
    while iter_count < max_iter:
        # Вычисляем значение функции в текущих точках
        f_x0 = f(x0)
        f_x1 = f(x1)

        # Проверяем, чтобы знаменатель не был равен нулю
        if abs(f_x1 - f_x0) < tol:
            raise ValueError("Разность значений функции слишком мала. Метод секущих не может быть применен.")

        # Вычисляем новое приближение
        x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Проверяем условие сходимости
        if abs(x_new - x1) < tol:
            print(f"Корень найден за {iter_count} итераций.")
            return x_new

        # Обновляем точки
        x0, x1 = x1, x_new
        iter_count += 1

    print(f"Достигнуто максимальное количество итераций ({max_iter}).")
    return x1

# root = secant_method(fun, 0, 0.5)

def secant_method(f, x0, x1, tol=1e-2, max_iter=100):
    """
    Находит корень уравнения f(x) = 0 методом секущих.

    Параметры:
    f: функция, корень которой нужно найти.
    x0, x1: начальные приближения.
    tol: допустимая погрешность (точность).
    max_iter: максимальное количество итераций.

    Возвращает:
    x: приближенное значение корня.
    """
    iter_count = 0
    while iter_count < max_iter:
        # Вычисляем значение функции в текущих точках
        f_x0 = f(x0)
        f_x1 = f(x1)

        # Проверяем, чтобы знаменатель не был равен нулю
        if abs(f_x1 - f_x0) < tol:
            raise ValueError("Разность значений функции слишком мала. Метод секущих не может быть применен.")

        # Вычисляем новое приближение
        x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        print(iter_count + 1, ":", round(x0, 3), round(x1, 3), round(x_new, 3), round(f(x_new), 3), round(abs(x_new - x1), 3))

        # Проверяем условие сходимости
        if abs(f(x_new)) < tol:
            print(f"Корень найден за {iter_count} итераций.")
            return x_new

        # Обновляем точки
        x0, x1 = x1, x_new
        iter_count += 1

    print(f"Достигнуто максимальное количество итераций ({max_iter}).")
    return x1

# root = secant_method(fun, 0, -0.5)
# print(f"Найденный корень: {root:.6f}")


# print(f"{y * 1/math.cos((x * y + 3/10)**2) - 2 * x}dx + {x + 1/math.cos((x * y + 3/10)**2)}dy = {x*x - math.tan(x * y + 3)}")
# print(f"{9/5 * x}dx + {4 * y}dy = {1 - 0.9 * x * x - 2 * y * y}")
x_old = 0.9
y_old = 0.4
x = x_old
y = y_old
e = 0.01
while True:
    dfdx = round(y * 1/math.cos((x * y + 3/10))**2 - 2 * x, 3)
    dfdy = round(x * 1/math.cos((x * y + 3/10))**2, 3)
    a = round(x*x - math.tan(x * y + 0.3), 3)

    dgdx = round(9/5 * x, 3)
    dgdy = round(4 * y, 3)
    b = round(1 - 0.9 * x * x - 2 * y * y, 3)

    A = np.array([[dfdx, dfdy], [dgdx, dgdy]])
    B = np.array([a, b])
    print("Система:")
    print(dfdx, dfdy, a)
    print(dgdx, dgdy, b)



    # Решаем систему линейных уравнений
    try:
        solution = np.linalg.solve(A, B)
        x_solution, y_solution = solution
        dx = round(x_solution, 3)
        dy = round(y_solution, 3)
        x += dx
        y += dy
        print(f"Решение системы: x = {x}, y = {y}")
        print(f"|{x} - {x_old}| = {abs(x - x_old)}")
        print(f"|{y} - {y_old}| = {abs(y - y_old)}")
        if abs(x - x_old) <= e and abs(y - y_old) <= e:
            print("Конец: ", x, y)
            break
        x_old = x
        y_old = y
    except np.linalg.LinAlgError:
        print("Система не имеет решения или матрица коэффициентов вырождена.")
