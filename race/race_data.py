from effects.effects_list import EffectsList # TODO


class RaceData:
    def __init__(self, name = None, desc = None, race_characteristics = None, effects = None)
        self.name = None
        if name != None:
            if not self.set_name(name):
                raise ValueError("Failed to set name in RaceData.")
            
        self.desc = None
        if desc != None:
            if not self.set_desc(desc):
                raise ValueError("Failed to set desc in RaceData.")
        
        self.race_characteristics = None
        if race_characteristics != None:
            if not self.set_race_characteristics(race_characteristics):
                raise ValueError("Failed to set race_characteristics in RaceData.")
        
        self.effects = None
        if effects != None:
            if not self.set_effects(effects):
                raise ValueError("Failed to set effects in RaceData.")
        
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
        def set_name(self, name):
            if isinstance(name, str):
                self.name = name
                return True
            
            return False
        
        def set_desc(self, desc):
            if isinstance(desc, str):
                self.desc = desc
                return True
            
            return False
        
        def set_race_characteristics(self, race_characteristics):
            if isinstance(race_characteristics, list):
                self.race_characteristics = race_characteristics
                return True
            
            return False
        
        def set_effects(self, effects):
            if isinstance(effects, EffectsList):
                self.effects = effects
                return True
                
            return False