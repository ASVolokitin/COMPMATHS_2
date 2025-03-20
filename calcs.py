# def parse_two_variable_function(func_str, variables):
#     if len(variables) != 2: return None
#     x, y = sp.symbols(variables)
#     try:
#         # Парсим строку в символьное выражение
#         func = sp.sympify(func_str)
#         return func
#     except sp.SympifyError as error:
#         print(f"Ошибка: {error}")
#         return None


