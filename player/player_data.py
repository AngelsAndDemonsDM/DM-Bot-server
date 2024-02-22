class PlayerData:
    def __init__(self):
        self.full_name # Полное ФИО персонажа
        self.id        # Уникальное ID персонажа
        self.height    # Рост
        self.weight    # Вес
        self.gender    # Пол
        self.race      # Раса
        self.needs     # Нужды персонажа
        
        self.characteristics # Характеристика

    def _set_attribute_within_range(self, attribute, value, min_value=None, max_value=None):
        """
        Устанавливает значение атрибута игрока в пределах допустимого диапазона.

        Args:
            attribute (str): Имя атрибута.
            value (int, float): Значение атрибута.
            min_value (int, float, None): Минимальное допустимое значение. Если None, то ограничение отсутствует.
            max_value (int, float, None): Максимальное допустимое значение. Если None, то ограничение отсутствует.

        Raises:
            TypeError: Если значение атрибута не является целым числом или числом с плавающей точкой.
        """
        if isinstance(value, (int, float)):
            value = float(value)
            if min_value is not None:
                value = max(value, min_value)
            if max_value is not None:
                value = min(value, max_value)
            setattr(self, attribute, value)
        else:
            raise TypeError(f"{attribute.capitalize()} must be an integer or a float")


    # Get методы
    def get_full_name(self):
        """
        Получение полного ФИО
        
        Args:
            None
        
        Returns:
            full_name (string): Полное ФИО
        """
        return self.full_name

    def get_id(self):
        """
        Получение ID игрока
        
        Args:
            None
        
        Returns:
            id (integer): ID игрока
        """
        return self.id

    def get_height(self):
        """
        Получение высоты игрока в метрах
        
        Args:
            None
        
        Returns:
            height (float): Высота игрока в метрах
        """
        return self.height

    def get_weight(self):
        """
        Получение веса игрока в килограммах
        
        Args:
            None
        
        Returns:
            weight (float): Вес игрока в килограммах
        """
        return self.weight
    
    def get_gender(self):
        """
        Получение пола игрока
        
        Args:
            None
        
        Returns:
            gender (string): Пола игрока
        """
        return self.gender
    
    def get_race(self):
        """
        Получение расы игрока
        
        Args:
            None
        
        Returns:
            race (RaceData): Раса игрока
        """
        return self.race

    def get_needs(self):
        """
        Получение нужд игрока
        
        Args:
            None
        
        Returns:
            needs(NeedsData): Нужды игрока
        """
        return self.needs

    def get_characteristics(self):
        """
        Получение характеристики игрока
        
        Args:
            None
        
        Returns:
            characteristics (CharacteristicsData): Характеристика игрока
        """
        return self.characteristics
    
    # Set методы
    def set_full_name(self, name):
        """
        Устанавливает ФИО игрока
        
        Args:
            name (string): ФИО игрока
        
        Returns:
            None
        """
        self.name = str(name)
    
    # ID - константа для сейв системы.

    def set_height(self, height):
        """
        Устанавливает рост игрока в метрах
        
        Args:
            height (integer, float): Высота игрока в метрах
        
        Returns:
            None
        """
        self._set_attribute_within_range('height', height, 0, None)

    def set_weight(self, weight):
        """
        Устанавливает вес игрока в килограммах
        
        Args:
            weight (integer, float): Вес игрока в килограммах
        
        Returns:
            None
        """
        self._set_attribute_within_range('weight', weight, 0, None)

    def set_gender(self, gender):
        """
        Устанавливает пол игрока
        
        Args:
            gender (string): Пол игрока
        
        Returns:
            None
        """
        self.gender = str(gender)

    def set_race(self, race):
        """
        Устанавливает расу игрока
        
        Args:
            race (RaceData): Раса игрока
        
        Returns:
            None
        """
        if isinstance(race, RaceData):
            self.race = race
        else:
            raise TypeError("Race must be a RaceData class.")

    def set_needs(self, )

    def set_characteristics(self, characteristics):
        """
        Устанавливает характеристику игрока
        
        Args:
            characteristics (CharacteristicsData): Характеристика игрока
        
        Returns:
            None
        """
        if isinstance(characteristics, CharacteristicsData):
            self.characteristics = characteristics
        else:
            raise TypeError("Characteristics must be a CharacteristicsData class")
