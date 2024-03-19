class Need:
    def __init__(self, id=None, name=None, desc=None, value=0, max_value=100, min_value=-100, count=-1):
        """
        Инициализация объекта Need.

        Args:
            id (str, optional): Идентификатор потребности. По умолчанию None.
            name (str, optional): Наименование потребности. По умолчанию None.
            desc (str, optional): Описание потребности. По умолчанию None.
            value (int, optional): Текущее значение потребности. По умолчанию 0.
            max_value (int, optional): Максимальное значение потребности. По умолчанию 100.
            min_value (int, optional): Минимальное значение потребности. По умолчанию -100.
            count (int, optional): Дельта изменения за ход/тик. По умолчанию -1.

        Raises:
            ValueError: Если сеттер не записал значение.
        """
        self.id = None
        if id is not None:
            if not self.set_id(id):
                raise ValueError(f"Failed to set id in {self.__class__.__name__}.")
        
        self.name = None
        if name is not None:
            if not self.set_name(name):
                raise ValueError(f"Failed to set name in {self.__class__.__name__}.")
        
        self.desc = None
        if desc is not None:
            if not self.set_desc(desc):
                raise ValueError(f"Failed to set desc in {self.__class__.__name__}.")
        
        self.max_value = None
        if max_value is not None:
            if not self.set_max(max_value):
                raise ValueError(f"Failed to set max_value in {self.__class__.__name__}.")
        
        self.min_value = None
        if min_value is not None:
            if not self.set_min(min_value):
                raise ValueError(f"Failed to set min_value in {self.__class__.__name__}.")
        
        self.value = None
        if value is not None:
            if not self.set_value(value):
                raise ValueError(f"Failed to set value in {self.__class__.__name__}.")
                
        self.count = None
        if count is not None:
            if not self.set_count(count):
                raise ValueError(f"Failed to set count in {self.__class__.__name__}.")

    # Get методы
    def get_id(self):
        """
        Получение идентификатора потребности.

        Returns:
            str: Идентификатор потребности.
        """
        return self.id
    
    def get_name(self):
        """
        Получение наименования потребности.

        Returns:
            str: Наименование потребности.
        """
        return self.name
    
    def get_desc(self):
        """
        Получение описания потребности.

        Returns:
            str: Описание потребности.
        """
        return self.desc
    
    def get_value(self):
        """
        Получение текущего значения потребности.

        Returns:
            int: Текущее значение потребности.
        """
        return self.value
    
    def get_max(self):
        """
        Получение максимального значения потребности.

        Returns:
            int: Максимальное значение потребности.
        """
        return self.max_value
    
    def get_min(self):
        """
        Получение минимального значения потребности.

        Returns:
            int: Минимальное значение потребности.
        """
        return self.min_value
    
    def get_count(self):
        """
        Получение дельты изменения за ход/тик.

        Returns:
            int: Дельта изменения за ход/тик.
        """
        return self.count
    
    # Set методы
    def set_id(self, id):
        """
        Установка идентификатора потребности.

        Args:
            id (str): Идентификатор потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(id, str):
            self.id = id
            return True
        
        return False
        
    def set_name(self, name):
        """
        Установка наименования потребности.

        Args:
            name (str): Наименование потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(name, str):
            self.name = name
            return True
        
        return False
        
    def set_desc(self, desc):
        """
        Установка описания потребности.

        Args:
            desc (str): Описание потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(desc, str):
            self.desc = desc
            return True
        
        return False
        
    def set_value(self, value):
        """
        Установка текущего значения потребности.

        Args:
            value (int): Текущее значение потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(value, int):
            if value > self.max_value:
                self.value = self.max_value
            elif value < self.min_value:
                self.value = self.min_value
            else:
                self.value = value
            return True
        
        return False 
        
    def set_max(self, max_value):
        """
        Установка максимального значения потребности.

        Args:
            max_value (int): Максимальное значение потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(max_value, int):
            self.max_value = max_value
            return True
        
        return False
        
    def set_min(self, min_value):
        """
        Установка минимального значения потребности.

        Args:
            min_value (int): Минимальное значение потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(min_value, int):
            self.min_value = min_value
            return True
        
        return False
        
    def set_count(self, count):
        """
        Установка дельты изменения за ход/тик.

        Args:
            count (int): Дельта изменения за ход/тик.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(count, int):
            self.count = count
            return True
        
        return False
    
    # Методы класса
    def update(self):
        """
        Изменение текущего значения потребности на значение дельты изменения за ход/тик.
        """
        temp = self.value
        temp += self.count
        self.set_value(temp)
        
    def value_change(self, number):
        """
        Изменение текущего значения потребности на указанное число.

        Args:
            number (int): Число, на которое изменяется текущее значение потребности.

        Raises:
            TypeError: Если тип параметра number не поддерживается.
        """
        if isinstance(number, int):
            temp = self.value
            temp += int(number)
            self.set_value(temp)
        else:
            raise TypeError("Number in value_change must be 'Integer' type")
