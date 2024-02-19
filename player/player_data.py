class PlayerData:
    def __init__(self):
        self.full_name # Полное ФИО персонажа
        self.id        # Уникальное ID персонажа
        self.height    # Рост
        self.weight    # Вес
        self.gender    # Пол
        self.race      # Раса
        
        self.health # Здоровье
        self.som    # Сила духа (strength of mind) (аналог маны)
        self.mind   # Рассудок
        self.hunger # Голод
        self.thirst # Жажда
        
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

    def get_health(self):
        """
        Получение здоровья игрока
        
        Args:
            None
        
        Returns:
            health (float): Здоровье игрока
        """
        return self.health

    def get_som(self):
        """
        Получение текущей силы духа
        
        Args:
            None
        
        Returns:
            som (float): Сила духа
        """
        return self.som
    
    def get_mind(self):
        """
        Получение рассудка игрока
        
        Args:
            None
        
        Returns:
            mind (float): Рассудок игрока
        """
        return self.mind
    
    def get_hunger(self):
        """
        Получение голода игрока
        
        Args:
            None
        
        Returns:
            hunger (float): Голод игрока
        """
        return self.hunger
    
    def get_thirst(self):
        """
        Получение жажды игрока
        
        Args:
            None
        
        Returns:
            thirst (float): Жажда игрока
        """
        return self.thirst
    
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

    def set_health(self, health):
        """
        Устанавливает здоровье игрока
        
        Args:
            health (integer, float): Здоровье игрока
        
        Returns:
            None
        """
        self._set_attribute_within_range('health', health, 0, None)

    def set_som(self, som):
        """
        Устанавливает силу духа игрока
        
        Args:
            som (integer, float): Сила духа
        
        Returns:
            None
        """
        self._set_attribute_within_range('som', som, None, None)

    def set_mind(self, mind):
        """
        Устанавливает рассудок игрока
        
        Args:
            mind (integer;float): Рассудок игрока
        
        Returns:
            None
        """
        self._set_attribute_within_range('mind', mind, -100, 100)

    def set_hunger(self, hunger):
        """
        Устанавливает голод игрока
        
        Args:
            hunger (integer;float): Голод игрока
        
        Returns:
            None
        """
        self._set_attribute_within_range('hunger', hunger, -100, 100)
    
    def set_thirst(self, thirst):
        """
        Устанавливает жажду игрока
        
        Args:
            thirst (integer;float): Жажда игрока
        
        Returns:
            None
        """
        self._set_attribute_within_range('thirst', thirst, -100, 100)

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
