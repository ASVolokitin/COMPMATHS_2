import math
import numdifftools as nd
import sympy as sp

ABOUT_NULL = 1e-6
MAX_INTERVAL_LENGTH = 1000000

def func1(x):
    return (x - 1)**2 - 1

def func2(x):
    return x**2 - 4

def func3(x): # e^x - 2
    try:
        res = math.exp(x) - 2
        return res
    except OverflowError:
        print(f"Ошибка: переполнение при вычислении exp({x})")
        return None

def func4(x):
    return math.sin(x)

def func5(x):
    return x**3 - 3*x + 1

def derivative(f, x):
    return nd.Derivative(f)(x)

def parse_function(func_str):
    x = sp.symbols('x')
    try:
        func = sp.sympify(func_str)
        return func
    except sp.SympifyError as error:
        print(f"Ошибка: {error}")
        return None

def input_int(prompt, valid_range=None):
    while True:
        try:
            user_input = int(input(prompt))
            if valid_range and user_input not in valid_range:
                print(f"Ошибка: введите число в пределах {valid_range}.")
            else:
                return user_input
        except ValueError:
            print("Ошибка: введено не число. Попробуйте снова.")

def input_float(prompt):
    while True:
        try:
            user_input = float(input(prompt).replace(",", "."))
            return user_input
        except ValueError:
            print("Ошибка: введено не число с плавающей точкой. Попробуйте снова.")

functions = {
    1: func1,
    2: func2,
    3: func3,
    4: func4,
    5: func5
}

func = functions[1]

def root_counter(a, b):
    n = 10000000
    if n > 1e9:
        print("Выбраннный интервал слишком велик, попробуйте уменьшить.")
        return -1
    root_cnt = 0
    length = ABOUT_NULL * 10000
    prev = func(a)
    cur = prev
    x = a
    while x <= b:
        cur = func(x)
        if cur == None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        if cur * prev < 0 or abs(cur) < ABOUT_NULL:
            print(f"Найдена смена знака функции (x = {x})")
            root_cnt += 1
        prev = cur
        x += length
        # print(x)
    return root_cnt

def half_division(a, b, e):
    n = 0 # Счётчик итераций
    x = (a + b) / 2
    while abs(b - a) >= e:
        fx = func(x)
        if abs(fx) < e: return x

        if func(a) * fx < 0: b = x
        else: a = x
        x = (a + b) / 2
        n += 1

    return x

def newton(a, b, e):
    x = (b + a) / 2
    for i in range(MAX_INTERVAL_LENGTH):
        df = derivative(func, x)

        if abs(df) < ABOUT_NULL:
            print("Производная слишком мала, метод Ньютона не применим.")
            return None

        x_new = x - func(x) / df
        if abs(x_new - x) < e:
            return x_new

        x = x_new
    return x

def main():
    print("Выберите функцию для анализа (введите число):")
    print("1: (x - 1)^2 - 1")
    print("2: x^2 - 4")
    print("3: exp(x) - 2")
    print("4: sin(x)")
    print("5: x^3 - 3x + 1")
    choice = input_int("Введите номер функции (1-5): ", valid_range={1, 2, 3, 4, 5})

    global func
    func = functions[choice]

    a = 0
    b = 0
    while True:
        a = input_float("Введите начало интервала (a): ")
        b = input_float("Введите конец интервала (b): ")

        if a >= b:
            print("Ошибка: начало интервала должно быть меньше конца. Попробуйте снова.")
            continue
        elif abs(b - a) > MAX_INTERVAL_LENGTH:
            print("Ошибка: выбран слишком большой интервал. Сократите (пожалуйста).")
            continue

        print("Определяю количество корней ...")
        roots = root_counter(a, b)
        if roots > 1:
            print(f"На выбранном интервале содержится более одного корня ({roots}), попробуйте сузить интервал.")
        elif roots == 1:
            print(f"На выбранном интервале найден единственный корень, ищу решение ...")
            break
        elif roots == 0:
            print("На выбранном интервале не найдено корней, попробуйте его изменить.")

    print("Метод половинного деления:", half_division(a, b, 0.00000005))
    print("Метод Ньютона:", newton(a, b, 0.00005))
    # print(derivative(func, 1))