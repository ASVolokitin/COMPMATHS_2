import sympy as sp

ABOUT_NULL = 1e-6
MAX_INTERVAL_LENGTH = 1000000

def parse_function(func_str):
    x = sp.symbols('x')
    try:
        func = sp.sympify(func_str)
        return func
    except sp.SympifyError as error:
        print(f"Ошибка: {error}")
        return None

def root_counter(a, b, func):
    n = 10000000
    root_cnt = 0
    length = ABOUT_NULL * 1000
    prev = func(a)
    cur = prev
    x = a
    print("Начинаю")
    while x <= b:
        cur = func(x)
        if cur == None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        if cur * prev < 0 or (abs(cur) < ABOUT_NULL and prev >= ABOUT_NULL):
            print(f"Найдена смена знака функции (x = {x})")
            root_cnt += 1
        prev = cur
        x += length
        # print(x)
    print("Проход завершён")
    return root_cnt