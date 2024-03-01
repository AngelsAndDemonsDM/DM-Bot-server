class OrganBase:
    def __init__(self, name = None, desc = None, max_hp = 100, efficiency = 100):
        self.name = None
        if name is not None:
            if not self.set_name(name):
                raise ValueError("Failed to set name in OrganBase.")
        
        self.desc = None
        if desc is not None:
            if not self.set_desc(desc):
                raise ValueError("Failed to set desc in OrganBase.")
        
        self.max_hp = 100
        if not self.set_max_hp(max_hp):
            raise ValueError("Failed to set max_hp in OrganBase.")
        
        self.hp = self.max_hp
        
        self.efficiency = 100
        if not self.set_efficiency(efficiency):
            raise ValueError("Failed to set efficiency in OrganBase.")
            
        self.effects = []
    
    # Get методы
    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc
    
    def get_max_hp(self):
        return self.max_hp
    
    def get_hp(self):
        return self.hp
    
    def get_efficiency(self):
        return self.efficiency
    
    def get_effects(self):
        return self.effects
    
    # Set методы
    def set_name(self, name):
        """
        Установка наименования таланта.

        Args:
            name (str): Наименование таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(name, str):
            self.name = name
            return True
            
        return False
        
    def set_desc(self, desc):
        """
        Установка описания таланта.

        Args:
            desc (str): Описание таланта.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(desc, str):
            self.desc = desc
            return True
            
        return False
    
    def set_max_hp(self, max_hp):
        if isinstance(max_hp, int):
            if max_hp < 0:
                self.max_hp = 0
            else: 
                self.max_hp = max_hp
            return True
        
        return False
    
    def set_hp(self, hp):
        if isinstance(hp, int):
            if hp > self.max_hp:
                self.hp = self.max_hp
            elif hp < 0:
                self.hp = 0
            else:
                self.hp = hp
            return True
        
        return False
    
    def set_efficiency(self, efficiency):
        if isinstance(efficiency, int):
            if efficiency < 0:
                self.efficiency = 0
            else: 
                self.efficiency = efficiency
            return True
        
        return False
    
    # Для эффектов
    def add_effect(self, effect):
        if isinstance(effect, Effect):
            if effect is not in self.effects:
                self.effects.append(effect)
                return True
        
        return False
    
    # Методы класса
    def update(self):
        raise NotImplementedError("BITCH CAN'T FUCKING WORK WITH OrganBase!")