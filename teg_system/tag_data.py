class TagData:
    def __init__(self, id=None):
        """
        Инициализация объекта TagData.

        Args:
            id (string, optional): Идентификатор тега. По умолчанию None.
        
        Raises:
            TypeError: Если тип переданного идентификатора не поддерживается.
        """
        if id is None:
            self.id = None
        elif not self.set_id(id):
            raise TypeError("Tag id in TagData must be a `string` type.")
    
    # Get методы
    def get_id(self):
        """
        Получение ID тега.

        Returns:
            id (string): ID тега.
        """
        return self.id

    # Set методы
    def set_id(self, id):
        """
        Установка ID тега.

        Args:
            id (string): ID тега.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(id, (str, int, float)):
            self.id = str(id)
            return True
        
        return False
