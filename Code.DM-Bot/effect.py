from etc.base_classes.base_object import BaseObject


class Effect(BaseObject):
    def __init__(self, id: str, name: str, description: str, type: str, strength: float, tick: int = -1):
        """
        Инициализация объекта эффекта.

        Args:
            type (str): Тип эффекта
            power (float): Сила эффекта.
            tick (int, optional): Количество тиков до завершения эффекта. По умолчанию -1.
        """
        super.__init__(id, name, description)
        self._type: str = type
        self._strength: float = strength
        self._tick: int = tick
    
    # Get metods
    @property
    def type(self) -> str:
        return self._type

    @property
    def strength(self) -> float:
        return self._strength
    
    @property
    def tick(self) -> str:
        return self._tick

    # Set metods
    @tick.setter
    def tick(self, value: int) -> None:
        if value <= -1:
            self._tick = -1
        
        self._tick = value

    # Class metods
    def update(self):
        """
        Обновление состояния эффекта.

        Returns:
            bool: True, если эффект еще активен, False, если эффект завершился.
        """
        if self._tick == -1:
            return True
        elif self._tick == 0:
            return False
        
        self._tick -= 1
        return True
