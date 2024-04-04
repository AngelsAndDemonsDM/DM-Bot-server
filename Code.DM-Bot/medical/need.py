from typing import Union


class Need:
    def __init__(self, id: str, name: str, description: str, max_value: int, value: int, min_value: int, count: int = -1):
        """
        Инициализация объекта Need.

        Args:
            id (str): Идентификатор потребности. 
            name (str): Наименование потребности. 
            desc (str): Описание потребности. 
            value (int): Текущее значение потребности. 
            max_value (int): Максимальное значение потребности. 
            min_value (int): Минимальное значение потребности.
            count (int, optional): Дельта изменения за ход/тик. По умолчанию -1.
        """
        self._id = id
        self._name = name
        self._description = description
        self._max_value = max_value
        self._value = value
        self._min_value = min_value
        self._count = count

    # Get методы
    @property
    def id(self) -> str:
        """
        Получение идентификатора потребности.

        Returns:
            str: Идентификатор потребности.
        """
        return self._id
    
    @property
    def name(self) -> str:
        """
        Получение наименования потребности.

        Returns:
            str: Наименование потребности.
        """
        return self._name
    
    @property
    def description(self) -> str:
        """
        Получение описания потребности.

        Returns:
            str: Описание потребности.
        """
        return self._description
    
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
    @id.setter
    def id(self, new_id: str):
        """
        Установка идентификатора потребности.

        Args:
            id (str): Идентификатор потребности.
        """
        self._id = str(new_id)
    
    @name.setter
    def name(self, new_name: str):
        """
        Установка наименования потребности.

        Args:
            name (str): Наименование потребности.
        """
        self._name = str(new_name)
    
    @description.setter
    def description(self, new_description):
        """
        Установка описания потребности.

        Args:
            desc (str): Описание потребности.
        """
        self._description = new_description
    
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
    
    # Методы класса
    def update(self):
        """
        Изменение текущего значения потребности на значение дельты изменения за ход/тик.
        """
        temp = self._value
        temp += self._count
        self.value = temp
        
    def value_change(self, number: Union[int, float]):
        """
        Изменение текущего значения потребности на указанное число.

        Args:
            number (int, float): Число, на которое изменяется текущее значение потребности.
        """
        number = int(number)

        temp = self._value
        temp += number
        self.value = temp
