from .medical_enums import GenderEnum, BreastSizeEnum

class OrgansSystem:
    def __init__(self):
        self.brain
        self.heart
        self.liver
        self.kidney
        self.lung
        self.stomach
        self.genitalia
        self.breast

class Organ:
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str = None):
        self._subtype = subtype
        self._id = id
        self._name = name
        self._description = description
        self._max_health = max_health
        self._standart_efficiency = standart_efficiency
        
        self._efficiency_per_health = standart_efficiency / max_health
        self._health = max_health
        self._efficiency = standart_efficiency
    
    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса.
        """
        if cls is Organ:
            raise NotImplementedError(f"You cannot create an abstract '{cls.__class__.__name__}' class. Use inheritance")
        return super().__new__(cls)
    
    def __str__(self):
        return f"subtype: {self._subtype}; id: {self._id}; name: {self._name}; desc: {self._description}; max_health: {self._max_health}; standart_efficiency: {self._standart_efficiency}; efficiency_per_health: {self._efficiency_per_health}; health: {self._health}; efficiency: {self._efficiency}"

    # Get metods
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description
    
    def get_max_health(self):
        return self._max_health

    def get_standart_efficiency(self):
        return self._standart_efficiency
    
    def get_efficiency_per_health(self):
        return self._efficiency_per_health
    
    def get_health(self):
        return self._health
    
    def get_efficiency(self):
        return self._efficiency

class Brain(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)

class Heart(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)

class Liver(Organ):    
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)

class Kidney(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)

class Lung(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        
    def __str__(self):
        return f"{super().__str__()};"

class Stomach(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, volume: float):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._volume = volume

    def __str__(self):
        return f"{super().__str__()}; volume: {self._volume}"

class Genitalia(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, gender_type: GenderEnum):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._gender_type = gender_type

    def __str__(self):
        return f"{super().__str__()}; gender_type: {self._gender_type}"

class Breast(Organ):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, size: BreastSizeEnum, reagent_per_day: int, reagent_per_tick: int, amount_reagent: int):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._size = size
        self._reagent_per_day = reagent_per_day
        self._reagent_per_tick = reagent_per_tick
        
        self._amount_reagent = amount_reagent

    def __str__(self):
        return f"{super().__str__()}; size: {self._size}; reagent_per_day: {self._reagent_per_day}; reagent_per_tick: {self._reagent_per_tick}; amount_reagent: {self._amount_reagent}"