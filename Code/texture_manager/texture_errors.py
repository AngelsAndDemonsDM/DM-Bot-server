from typing import List


class SpriteValidationError(Exception):
    """Базовый класс для исключений, связанных с валидацией спрайтов.

    Этот класс расширяет стандартный класс исключений и добавляет дополнительную информацию о пути к файлу, где произошла ошибка.

    Args:
        message (str): Сообщение об ошибке, описывающее, что пошло не так.
        path (str): Путь к файлу, в котором произошла ошибка.
    """
    def __init__(self, message: str, path: str):
        super().__init__(message)
        self.message = message
        self.path = path

class InvalidSpriteError(SpriteValidationError):
    """Исключение для случаев, когда файл info.yml отсутствует или содержит неверные данные.

    Этот класс расширяет SpriteValidationError и добавляет информацию о недостающих файлах или полях.

    Args:
        message (str): Сообщение об ошибке, описывающее, что пошло не так.
        path (str): Путь к файлу, в котором произошла ошибка.
        missing_files (List[str], optional): Список недостающих файлов. По умолчанию None.
        missing_field (str, optional): Отсутствующее поле в файле info.yml. По умолчанию None.
    """
    def __init__(self, message: str, path: str, missing_files: List[str] = None, missing_field: str = None):
        super().__init__(message, path)
        self.missing_files = missing_files
        self.missing_field = missing_field
