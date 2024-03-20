from typing import Union
from .body import Body


class Mind:
    def __init__(self, id: str, body: Body):
        """
        Инициализация объекта Mind.

        Args:
            id (str, optional): Идентификатор разума. По умолчанию None.
            body (Body, optional): TODO. По умолчанию None.
        """
        self.id = id
        self.body = body
        
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
    def set_id(self, id: Union[str, int, float]):
        """
        Установка идентификатора разума.

        Args:
            id (str, int, float): Идентификатор разума.
        """
        self.id = id
        
    def set_body(self, body: Body):
        """
        """
        self.body = body
