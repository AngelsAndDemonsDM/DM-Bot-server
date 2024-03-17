class Effect:
    def __init__(self, effect_id=None, power=None, tick=-1):
        """
        Инициализация объекта эффекта.

        Args:
            effect_id (str, optional): Идентификатор эффекта. По умолчанию None.
            power (float, optional): Сила эффекта. По умолчанию None.
            tick (int, optional): Количество тактов до завершения эффекта. По умолчанию -1.

        Raises:
            ValueError: Если сеттер не смог установить значение.
        """
        self.effect_id = None
        if effect_id is not None:
            if not self.set_effect_id(effect_id):
                raise ValueError(f"Failed to set effect_id in {self.__class__.__name__} in init.")
            
        self.strength = None
        if power is not None:
            if not self.set_strength(power):
                raise ValueError(f"Failed to set strength in {self.__class__.__name__} in init.")
        
        self.tick = None
        if tick != -1:
            if not self.set_tick(tick):
                raise ValueError(f"Failed to set tick in {self.__class__.__name__} in init")
    
    def update(self):
        """
        Обновление состояния эффекта.

        Returns:
            bool: True, если эффект еще активен, False, если эффект завершился.
        """
        if self.tick == -1:
            return True
        elif self.tick == 0:
            return False
        
        self.tick -= 1
        return True
    
    def set_effect_id(self, new_effect_id):
        """
        Установка идентификатора эффекта.

        Args:
            new_effect_id (str): Новый идентификатор эффекта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        self.effect_id = str(new_effect_id)
        return True
    
    def set_strength(self, new_strength):
        """
        Установка силы эффекта.

        Args:
            new_strength (float): Новое значение силы эффекта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(new_strength, (int, float)):
            self.strength = float(new_strength)
            return True
        
        return False
    
    def set_tick(self, new_tick):
        """
        Установка количества тактов до завершения эффекта.

        Args:
            new_tick (int): Новое количество тактов до завершения эффекта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(new_tick, (int, float)):
            new_tick = int(new_tick)
            if new_tick < -1:
                self.tick = -1
            else:
                self.tick = new_tick
            return True
            
        return False
        
    def get_tick(self):
        """
        Получение количества тактов до завершения эффекта.

        Returns:
            int: Количество тактов до завершения эффекта.
        """
        return self.tick
    
    def get_effect_id(self):
        """
        Получение идентификатора эффекта.

        Returns:
            str: Идентификатор эффекта.
        """
        return self.effect_id
    
    def get_strength(self):
        """
        Получение силы эффекта.

        Returns:
            float: Сила эффекта.
        """
        return self.strength
    
    def get_cur_effect(self):
        """
        Получение текущего состояния эффекта в виде списка.

        Returns:
            list: [effect_id, strength], текущее состояние эффекта.
        """
        return [self.effect_id, self.strength]
