from .effect import Effect  # Импорт класса Effect из модуля effect


class EffectManager:
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
    
    def f_add_effect(self, new_effect):
        """
        Добавление нового эффекта в список.

        Args:
            new_effect (Effect): Новый эффект для добавления.

        Returns:
            bool: True, если эффект был успешно добавлен, в противном случае False.
        """
        if isinstance(new_effect, Effect):
            self.effect_list.append(new_effect)
            return True
        
        return False
    
    def add_effect(self, new_effect):
        """
        Добавление нового эффекта в список, если его effect_id отсутствует.

        Args:
            new_effect (Effect): Новый эффект для добавления.

        Returns:
            bool: True, если эффект был успешно добавлен, в противном случае False.
        """
        if isinstance(new_effect, Effect):
            if not any(obj.effect_id == new_effect.effect_id for obj in self.effect_list):
                self.effect_list.append(new_effect)
                return True
                
        return False
    
    def remove_effect(self, effect_id):
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
