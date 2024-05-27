from base_classes.base_object import BaseObject


class Effect(BaseObject):
    def __init__(self, id: str, name: str, description: str, strength: int, tick: int = -1):
        """
        Инициализация объекта эффекта.

        Args:
            power (float): Сила эффекта.
            tick (int, optional): Количество тиков до завершения эффекта. По умолчанию -1.
        """
        super.__init__(id, name, description)
        self._strength = strength
        self._tick = tick
    
    # Get metods
    @property
    def strength(self) -> str:
        return self._strength
    
    @property
    def tick(self) -> str:
        return self._tick

    # Set metods
    @tick.setter
    def tick(self, value: int):
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
