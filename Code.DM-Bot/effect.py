class Effect:
    def __init__(self, id: str, name: str, description: str, strength: int, tick: int = -1):
        """
        Инициализация объекта эффекта.

        Args:
            id (str, optional): Идентификатор эффекта. По умолчанию None.
            power (float, optional): Сила эффекта. По умолчанию None.
            tick (int, optional): Количество тактов до завершения эффекта. По умолчанию -1.
        """
        self._id = id
        self._name = name
        self._description = description
        self._strength = strength
        self._tick = tick
    
    # get metods
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def strength(self) -> str:
        return self._strength
    
    @property
    def tick(self) -> str:
        return self._tick

    # set metods
    @id.setter
    def id(self, value: str):
        self._id = value

    @name.setter
    def name(self, value: str):
        self._name = value

    @description.setter
    def description(self, value: str):
        self._description = value

    @tick.setter
    def tick(self, value: int):
        if value <= -1:
            self._tick = -1
        
        self._tick = value


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
