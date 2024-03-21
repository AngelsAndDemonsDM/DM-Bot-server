from typing import Union

from .effect import EffectsList


class Race:
    def __init__(self, name: str, desc: str, race_characteristics: list, effects: EffectsList):
        self.name = name
        self.desc = desc
        self.race_characteristics = race_characteristics
        self.effects = effects
        
        # Get metods
        def get_name(self):
            return self.name
        
        def get_desc(self):
            return self.desc
        
        def get_race_characteristics(self):
            return self.race_characteristics
        
        def get_effects(self):
            return self.effects
        
        # Set metods
        def set_name(self, name: Union[str, int, float]):
            self.name = str(name)
        
        def set_desc(self, desc: Union[str, int, float]):
            self.desc = desc
        
        def set_race_characteristics(self, race_characteristics: list):
            self.race_characteristics = race_characteristics
        
        def set_effects(self, effects: EffectsList):
            self.effects = effects