class PrototypeError(Exception):
    __slots__ = ['file_path', 'location', 'message']

    def __init__(self, file_path: str, location: str, message: str) -> None:
        """
        Исключение, возникающее при ошибке в прототипах.

        Args:
            file_path (str): Путь к файлу с ошибкой.
            location (str): Место в файле, где возникла ошибка.
            message (str): Описание ошибки.
        """
        self.file_path = file_path
        self.location = location
        self.message = message
        super().__init__(f"Error in file '{file_path}' at '{location}': {message}")
