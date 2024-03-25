from typing import Union


class Effect: # ПЕРЕДЕЛАТЬ
    def __init__(self, effect_id: str, power: int, tick: int):
        """
        Инициализация объекта эффекта.

        Args:
            effect_id (str, optional): Идентификатор эффекта. По умолчанию None.
            power (float, optional): Сила эффекта. По умолчанию None.
            tick (int, optional): Количество тактов до завершения эффекта. По умолчанию -1.
        """
        self._effect_id = effect_id
        self.strength = power
        self.tick = tick
    
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
    
    def set_effect_id(self, new_effect_id: Union[str, int, float]):
        """
        Установка идентификатора эффекта.

        Args:
            new_effect_id (str, int, float): Новый идентификатор эффекта.
        """
        self.effect_id = str(new_effect_id)

    def set_strength(self, new_strength: Union[int, float]):
        """
        Установка силы эффекта.

        Args:
            new_strength (int, float): Новое значение силы эффекта.
        """
        self.strength = float(new_strength)

    def set_tick(self, new_tick: Union[int, float]):
        """
        Установка количества тактов до завершения эффекта.

        Args:
            new_tick (int): Новое количество тактов до завершения эффекта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        new_tick = int(new_tick)
        if new_tick < -1:
            self.tick = -1
        else:
            self.tick = new_tick            
        
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

class EffectManager: # ПЕРЕДЕЛАТЬ
    def __init__(self):
        """
        Инициализация менеджера эффектов.

        Создает пустой список для хранения эффектов.
        """
        self.effect_list = []
    
    def update(self):
        """
        Обновление эффектов.

        Вызывает метод update() для каждого эффекта в списке.
        Если метод update() возвращает False, эффект удаляется из списка.
        """
        for effect in self.effect_list:
            if not effect.update():
                del effect
    
    def f_add_effect(self, new_effect: Effect):
        """
        Добавление нового эффекта в список.

        Args:
            new_effect (Effect): Новый эффект для добавления.
        """
        self.effect_list.append(new_effect)
    
    def add_effect(self, new_effect: Effect):
        """
        Добавление нового эффекта в список, если его effect_id отсутствует.

        Args:
            new_effect (Effect): Новый эффект для добавления.

        Returns:
            bool: True, если эффект был успешно добавлен, в противном случае False.
        """
        if not any(obj.effect_id == new_effect.effect_id for obj in self.effect_list):
            self.effect_list.append(new_effect)
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
        for effect in self.effect_list:
            if effect.effect_id == effect_id:
                self.effect_list.remove(effect)
                return True
        
        return False
    
    def get_all_effects(self):
        """
        Получение списка всех эффектов.

        Returns:
            list: Список всех эффектов.
        """
        return self.effect_list
    
    def get_all_effects_in_list(self):
        """
        Получение списка, содержащего информацию о каждом эффекте в формате [effect_id, strength].

        Returns:
            list: Список, содержащий информацию о каждом эффекте.
        """
        get_list = []
        for effect in self.effect_list:
            get_list.append(effect.get_cur_effect())
        
        return get_list
