from .body.body import Body


class Mind:
    def __init__(self, id=None, body=None):
        """
        Инициализация объекта Mind.

        Args:
            id (str, optional): Идентификатор разума. По умолчанию None.
            body (Body, optional): TODO. По умолчанию None.

        Raises:
            ValueError: Если сеттер не записал значение.
        """
        self.id = None
        if id is not None:
            if not self.set_id(id):
                raise ValueError("Failed to set id in Mind.")
        
        self.body = None
        if body is not None:
            if not self.set_body(body):
                raise ValueError("Failed to set body in Mind.")
        
    # Get методы
    def get_id(self):
        """
        Получение идентификатора разума.

        Returns:
            str: Идентификатор разума.
        """
        return self.id
    
    def get_body(self):
        """
        """
        return self.body
    
    # Set методы
    def set_id(self, id):
        """
        Установка идентификатора разума.

        Args:
            id (str): Идентификатор разума.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(id, str):
            self.id = id
            return True
        
        return False

    def set_body(self, body):
        """
        """
        if isinstance(body, Body):
            self.body = body
            return True
        
        return False