import numpy as np

from entites.equation_system import System1, System2, System3

ABOUT_NULL = 1e-2
MAX_INTERVAL_LENGTH = 1000000
MIN_INTERVAL_LENGTH = 0.5
SAMPLES_AMOUNT = 1000
MAX_ITERATIONS = 100000

system_functions_options = [System1(), System2(), System3()]

def df(func, x):
    dx = 0.0001
    return (func(x + dx) - func(x - dx)) / (2 * dx)

def dff(func, x):
    dx = 0.0001
    return (func(x + dx) - 2 * func(x) + func(x - dx)) / dx ** 2

def result_dict(root, value, iter_amout, status_msg):
    if root is None or value is None:
        root = None
        value = None
        iter_amout = 0
    return {"root": root, "value": value, "iter_amount": iter_amout, "status_msg": status_msg}

def root_counter(a, b, func):
    n = 1000000
    root_cnt = 0
    length = ABOUT_NULL * 100
    prev = func(a)
    cur = prev
    x = a
    print("Обход начат")
    while x <= b + ABOUT_NULL:
        cur = func(x)
        if cur == None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        # if cur * prev < 0 or (abs(cur) < ABOUT_NULL and prev >= ABOUT_NULL and (cur - prev >= ABOUT_NULL * 10000)):
        if cur * prev < 0 or abs(cur) < ABOUT_NULL:
            print(f"Найдена смена знака функции (x = {x})")
            root_cnt += 1
            if abs(cur) < ABOUT_NULL:
                print(cur)
                cur = 0
        prev = cur
        x += length
    print("Обход завершён")
    print(root_cnt)
    return root_cnt

def find_derivative_abs_max(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    return max(abs(df(func, x_vals)))

def find_func_abs_max(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    return max(abs(func(x_vals)))

def load_stylesheet(filename):
    """Загружает стили из CSS-файла."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()