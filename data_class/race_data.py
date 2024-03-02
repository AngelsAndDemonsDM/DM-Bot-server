# TODO:
# Влияние на статы

# Таланты расы
class Talant:
    def __init__(self, id=None, name=None, desc=None, tags=None):     
        """
        Инициализация объекта Talant.

        Args:
            id (str, optional): Идентификатор таланта. По умолчанию None.
            name (str, optional): Наименование таланта. По умолчанию None.
            desc (str, optional): Описание таланта. По умолчанию None.
            tags (list, optional): Список тегов для таланта. По умолчанию None.

        Raises:
            ValueError: Если сеттер не записал значение.
        """
        self.id = None
        if id is not None:
            if not self.set_id(id):
                raise ValueError("Failed to set id in Talant.")
        
        self.name = None
        if name is not None:
            if not self.set_name(name):
                raise ValueError("Failed to set name in Talant.")
        
        self.desc = None
        if desc is not None:
            if not self.set_desc(desc):
                raise ValueError("Failed to set desc in Talant.")
        
        self.tags = None
        if tags is not None:
            if not self.set_tags(tags):
                raise ValueError("Failed to set tags in Talant.")
    
    # Get методы
    def get_id(self):
        """
        Получение идентификатора таланта.

        Returns:
            str: Идентификатор таланта.
        """
        return self.id
    
    def get_name(self):
        """
        Получение наименования таланта.

        Returns:
            str: Наименование таланта.
        """
        return self.name
    
    def get_desc(self):
        """
        Получение описания таланта.

        Returns:
            str: Описание таланта.
        """
        return self.desc
    
    def get_tags(self):
        """
        Получение списка тегов таланта.

        Returns:
            list: Список тегов таланта.
        """
        return self.tags
     
    # Set методы
    def set_id(self, id):
        """
        Установка идентификатора таланта.

        Args:
            id (str): Идентификатор таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(id, str):
            self.id = id
            return True
            
        return False
    
    def set_name(self, name):
        """
        Установка наименования таланта.

        Args:
            name (str): Наименование таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(name, str):
            self.name = name
            return True
            
        return False
        
    def set_desc(self, desc):
        """
        Установка описания таланта.

        Args:
            desc (str): Описание таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(desc, str):
            self.desc = desc
            return True
            
        return False
        
    def set_tags(self, tags):
        """
        Установка списка тегов таланта.

        Args:
            tags (list): Список тегов таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(tags, list):
            self.tags = tags
            return True
            
        return False

# Особенности расы
class Notable:
    def __init__(self, id = None, name = None, desc = None, tags = None):
     """
        Инициализация объекта Notable.

        Args:
            id (str, optional): Идентификатор особенности. По умолчанию None.
            name (str, optional): Наименование особенности. По умолчанию None.
            desc (str, optional): Описание особенности. По умолчанию None.
            tags (list, optional): Список тегов для особенности. По умолчанию None.

        Raises:
            ValueError: Если сеттер не записал значение.
    """
        self.id = None
        if id is not None:
            if not self.set_id(id):
                raise ValueError("Failed to set id in Notable")
                
        self.name = None
        if name is not None:
            if not self.set_name(name):
                raise ValueError("Failed to set name in Notable")
                
        self.desc = None
        if desc is not None:
            if not self.set_desc(desc):
                raise ValueError("Failed to set desc in Notable")
                
        self.tags = None
        if tags is not None:
            if not self.set_tags(tags):
                raise ValueError("Failed to set tags in Notable")

    # Get методы
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
        
    def get_desc(self):
        return self.desc
        
    def get_tags(self):
        return self.tags
        
    # Set методы
    def set_id(self, id):
        if isinstance(id, (str, int, float)):
            self.set = set
            return True
            
    return False
    
    def set_name(self, name):
        if isinstance(name, (str, int, float)):
            self.name = name
            return True 
           
    return False
    
    def set_desc(self, desc):
        if isinstance(desc, (str, int, float)):
            self.desc = desc
            return True
            
    return False
    
    def set_tags(self, tags):
        if isinstance(tags, list):
            self.tags = tags
            return True
            
    return False
    
# Влияние на статы
class Stat:
    def __init__(self, id = None, name = None, desc = None, bonus = 0)
    """
        Инициализация объекта Stat.

        Args:
            id (str, optional): Идентификатор влияние. По умолчанию None.
            name (str, optional): Наименование влияние. По умолчанию None.
            desc (str, optional): Описание влияние. По умолчанию None.
            bonus (int, optional): Числовое влияние на характеристику. По умолчанию 0.
            
        Raises:
            ValueError: Если сеттер не записал значение.
    """
    
    self.id = None
    if id is not None:
        if not self.set_id(id):
            raise ValueError("Failed to set id in Stat.")
            
    self.name = None
    if name is not None:
        if not self.set_name(name):
            raise ValueError("Failed to set name in Stat.")
            
    self.desc = None
    if desc is not None:
        if not self.set_desc(desc):
            raise ValueError("Failed to set desc in Stat.")
            
    self.bonus = None
    if bonus is not None:
        if not self.set_bonus(desc):
            raise ValueError("Failed to set bonus in Stat.")
    
            
    # Get методы
    def get_id(self):
        return(self.id)
        
    def get_name(self):
        return self.name
        
    def get_desc(self):
        return self.name
        
    def get_bonus(self):
        return self.bonus
        
    # Set методы
    def set_id(self, id):
        if isinstance(id, (str, int, float)):
            self.id = id
            return True
            
    return False
    
    def set_name(self, name):
        if isinstance(name, (str, int, float)):
            self.name = name
            return True
    
    return False
    
    def set_desc(self, desc):
        if isinstance(desc, (str, int, float)):
            self.desc = desc
            return True
            
    return False
    
    def set_bonus(self, bonus):
        if isinstance(bonus, int):
            self.bonus = bonus
            return True
            
    return False

# Нужды расы
class Needs:
    def __init__(self, id=None, name=None, desc=None, value=0, max=100, min=-100, count=-1):
        """
        Инициализация объекта Needs.

        Args:
            id (str, optional): Идентификатор потребности. По умолчанию None.
            name (str, optional): Наименование потребности. По умолчанию None.
            desc (str, optional): Описание потребности. По умолчанию None.
            value (int, optional): Текущее значение потребности. По умолчанию 0.
            max (int, optional): Максимальное значение потребности. По умолчанию 100.
            min (int, optional): Минимальное значение потребности. По умолчанию -100.
            count (int, optional): Дельта изменения за ход/тик. По умолчанию -1.

        Raises:
            ValueError: Если сеттер не записал значение.
        """
        self.id = None
        if id is not None:
            if not self.set_id(id):
                raise ValueError("Failed to set id in Needs.")
        
        self.name = None
        if name is not None:
            if not self.set_name(name):
                raise ValueError("Failed to set name in Needs.")
        
        self.desc = None
        if desc is not None:
            if not self.set_desc(desc):
                raise ValueError("Failed to set desc in Needs.")
        
        self.max = None
        if max is not None:
            if not self.set_max(max):
                raise ValueError("Failed to set max in Needs.")
        
        self.min = None
        if min is not None:
            if not self.set_min(min):
                raise ValueError("Failed to set min in Needs.")
        
        self.value = None
        if value is not None:
            if not self.set_value(value):
                raise ValueError("Failed to set value in Needs.")
                
        self.count = None
        if count is not None:
            if not self.set_count(count):
                raise ValueError("Failed to set count in Needs.")

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
        return self.max
    
    def get_min(self):
        """
        Получение минимального значения потребности.

        Returns:
            int: Минимальное значение потребности.
        """
        return self.min
    
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
            if value > self.max:
                self.value = self.max
            elif value < self.min:
                self.value = self.min
            else:
                self.value = value
            return True
        
        return False 
        
    def set_max(self, max):
        """
        Установка максимального значения потребности.

        Args:
            max (int): Максимальное значение потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(max, int):
            self.max = max
            return True
        
        return False
        
    def set_min(self, min):
        """
        Установка минимального значения потребности.

        Args:
            min (int): Минимальное значение потребности.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(min, int):
            self.min = min
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
        
    def uptake(self):
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
