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

class EffectManager:
    def __init__(self):
        """
        Инициализация менеджера эффектов.

        Создает пустой список для хранения эффектов.
        """
        self._effect_list = []
    
    def update(self):
        """
        Обновление эффектов.

        Вызывает метод update() для каждого эффекта в списке.
        Если метод update() возвращает False, эффект удаляется из списка.
        """
        for effect in self._effect_list:
            if not effect.update():
                del effect
    
    def f_add_effect(self, new_effect: Effect):
        """
        Добавление нового эффекта в список.

        Args:
            new_effect (Effect): Новый эффект для добавления.
        """
        self._effect_list.append(new_effect)
    
    def add_effect(self, new_effect: Effect):
        """
        Добавление нового эффекта в список, если его effect_id отсутствует.

        Args:
            new_effect (Effect): Новый эффект для добавления.

        Returns:
            bool: True, если эффект был успешно добавлен, в противном случае False.
        """
        if not any(obj.effect_id == new_effect.effect_id for obj in self._effect_list):
            self._effect_list.append(new_effect)
            return True
                
        return False
    
    def remove_effect(self, effect_id: str):
        """
        Удаление эффекта из списка по его effect_id.

        Args:
            effect_id (str): ID эффекта, который требуется удалить.

        Returns:
            bool: True, если эффект был успешно удален, в противном случае False.
        """
        for effect in self._effect_list:
            if effect.effect_id == effect_id:
                self._effect_list.remove(effect)
                return True
        
        return False
    
    @property
    def effects(self):
        """
        Получение списка всех эффектов.

        Returns:
            list: Список всех эффектов.
        """
        return self._effect_list
