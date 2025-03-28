import json
class json_parser:
    @staticmethod
    def read_json(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ошибка парсинга JSON: {e}", e.doc, e.pos)
        except Exception as e:
            raise ValueError(f"Ошибка чтения файла: {str(e)}")

    @staticmethod
    def parse_equation(data):
        required_fields = ["x_left", "x_right", "accuracy"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        try:
            x_left = float(data["x_left"])
            x_right = float(data["x_right"])
            accuracy = float(data["accuracy"])
        except (ValueError, TypeError):
            raise ValueError("Поля x_left, x_right и accuracy должны быть числами.")

        if x_left >= x_right:
            raise ValueError("x_left должен быть меньше x_right.")

        if accuracy <= 0:
            raise ValueError("Точность должна быть положительным числом.")

        return {
            "x_left_border": x_left,
            "x_right_border": x_right,
            "accuracy": accuracy
        }

    @staticmethod
    def parse_system(data):
        required_fields = ["x_left", "x_right", "y_bottom", "y_top", "x_start", "y_start"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        try:
            x_left = float(data["x_left"])
            x_right = float(data["x_right"])
            y_bottom = float(data["y_bottom"])
            y_top = float(data["y_top"])
            x_start = float(data["x_start"])
            y_start = float(data["y_start"])
        except (ValueError, TypeError):
            raise ValueError("Все числовые поля должны быть числами.")

        if x_left >= x_right:
            raise ValueError("x_left должен быть меньше x_right.")

        if y_bottom >= y_top:
            raise ValueError("y_bottom должен быть меньше y_top.")

        if not (x_left <= x_start <= x_right) or not (y_bottom <= y_start <= y_top):
            return ValueError("Начальное приближение должно находиться в пределах границ интервала")

        return {
            "x_left_border": x_left,
            "x_right_border": x_right,
            "y_bottom_border": y_bottom,
            "y_top_border": y_top,
            "x_start": x_start,
            "y_start": y_start
        }
