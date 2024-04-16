from etc.base_classes.base_object import BaseObject


class Need(BaseObject):
    def __init__(self, id: str, name: str, description: str, max_value: int, value: int, min_value: int, count: int = -1):
        """
        Инициализация объекта Need.
        Наследуется от BaseObject.

        Attributes:
            value (int): Текущее значение потребности. 
            max_value (int): Максимальное значение потребности. 
            min_value (int): Минимальное значение потребности.
            count (int, optional): Дельта изменения за ход/тик. По умолчанию -1.
        """
        super().__init__(id, name, description)
        self._max_value = max_value
        self._value = value
        self._min_value = min_value
        self._count = count

    # Get методы
    @property
    def value(self) -> int:
        """
        Получение текущего значения потребности.

        Returns:
            int: Текущее значение потребности.
        """
        return self._value
    
    @property
    def max_value(self) -> int:
        """
        Получение максимального значения потребности.

        Returns:
            int: Максимальное значение потребности.
        """
        return self._max_value
    
    @property
    def min_value(self) -> int:
        """
        Получение минимального значения потребности.

        Returns:
            int: Минимальное значение потребности.
        """
        return self._min_value
    
    @property
    def count(self) -> int:
        """
        Получение дельты изменения за ход/тик.

        Returns:
            int: Дельта изменения за ход/тик.
        """
        return self._count
    
    # Set методы
    @value.setter
    def value(self, new_value: int):
        """
        Установка текущего значения потребности.

        Args:
            value (int): Текущее значение потребности.
        """
        if new_value > self._max_value:
            self._value = self._max_value
        elif new_value < self._min_value:
            self._value = self._min_value
        
        self._value = new_value
    
    @max_value.setter
    def max_value(self, new_max_value: int):
        """
        Установка максимального значения потребности.

        Args:
            max_value (int): Максимальное значение потребности.
        """
        self._max_value = new_max_value

    @min_value.setter 
    def min_value(self, new_min_value: int):
        """
        Установка минимального значения потребности.

        Args:
            min_value (int): Минимальное значение потребности.
        """
        self._min_value = new_min_value

    
    @count.setter
    def set_count(self, new_count: int):
        """
        Установка дельты изменения за ход/тик.

        Args:
            count (int): Дельта изменения за ход/тик.
        """
        self._count = new_count
    
    # Class metods
    def update(self):
        """
        Изменение текущего значения потребности на значение дельты изменения за ход/тик.
        """
        temp = self._value
        temp += self._count
        self.value = temp
        
    def value_change(self, value: int):
        """
        Изменение текущего значения потребности на указанное число.

        Args:
            value (int): Число, на которое изменяется текущее значение потребности.
        """
        temp = self._value
        temp += value
        self.value = temp
