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
        
        self.characteristics # Характеристики
    
    # Get методы
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_full_name(self):
        return self.full_name

    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_id(self):
        return self.id

    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_height(self):
        return self.height

    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_weight(self):
        return self.weight
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_gender(self):
        return self.gender
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_race(self):
        return self.race

    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_health(self):
        return self.health

    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_som(self):
        return self.som
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_mind(self):
        return self.mind
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_hunger(self):
        return self.hunger
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_thirst(self):
        return self.thirst
    
    """
    desc
    
    Args:
        None
    
    Returns:
        None
    """
    def get_characteristics(self):
        return self.characteristics
    
    # Set методы
    def set_full_name(self, name):
        self.name = str(name)
    
    # ID - константа для сейв системы.

    def set_height(self, height):
        if isinstance(height, (int, float)):
            self.height = float(height)
        else:
            raise TypeError("Height must be an integer or a float.")

    def set_weight(self, weight):
        if isinstance(weight, (int, float)):
            if float(weight) < 0:
                self.weight = 0.0
            else:
                self.weight = float(weight)
        else:
            raise TypeError("Weight must be an integer or a float.")

    def set_gender(self, gender):
        self.gender = gender

    def set_race(self, race):
        if isinstance(race, RaceData):
            self.race = race
        else:
            raise TypeError("Race must be a RaceData class.")
    
    def set_health(self, health):
        if isinstance(health, (int, float)):
            if float(health) < 0:
                self.health = 0.0
            else:
                self.health = float(health)
        else:
            raise TypeError("Health must be an integer or a float.")
    
    def set_som(self, som):
        if isinstance(som, (int, float)):
            self.som = float(som)
        else:
            raise TypeError("Som must be an integer or a float")
    
    def set_mind(self, mind):
        if isinstance(mind, (int, float)):
            if float(mind) < -100:
                self.mind = -100.0
            elif float(mind) > 100:
                self.mind = 100.0
            else:
                self.mind = float(mind)
        else:
            raise TypeError("Mind must be an integer or a float")
    
    def set_hunger(self, hunger):
        if isinstance(hunger, (int, float)):
            if float(hunger) < -100:
                self.hunger = -100.0
            elif float(hunger) > 100:
                self.hunger = 100.0
            else:
                self.hunger = float(hunger)
        else:
            raise TypeError("Hunger must be an integer or a float")

    def set_thirst(self, thirst):
        if isinstance(thirst, (int, float)):
            if float(thirst) < -100:
                self.thirst = -100.0
            elif float(thirst) > 100:
                self.thirst = 100.0
            else:
                self.thirst = float(thirst)
        else:
            raise TypeError("Thirst must be an integer or a float")
        
    def set_characteristics(self, characteristics):
        if isinstance(characteristics, CharacteristicsData):
            self.characteristics = characteristics
        else:
            raise TypeError("Characteristics must be a CharacteristicsData class")
