from race.race_data import RaceData

class Body:
    def __init__(self, race = None, gender = None, specialization = None, stats = None, body_effects = None, body_items = None, body_medical = None):
        self.race = None 
        if race != None:
            if not self.set_race(race):
                raise ValueError(f"Failed to set race in {self.__class__.__name__}.")
                
        self.gender = None
        if gender is not None:
            if not self.set_gender(gender):
                raise ValueError(f"Failed to set gender in {self.__class__.__name__}.")
                       
                       
        self.specialization = None 
        if specialization is not None: 
            if not self.set_specialization(specialization):
                raise ValueError(f"Failed to set specialization in {self.__class__.__name__}.")
        
        self.stats = None 
        if stats is not None:
            if not self.set_stats(stats):
                raise ValueError(f"Failed to set stats in {self.__class__.__name__}.")
        
        
        self.body_effects = None 
        
        self.body_items = None 
        
        self.body_medical = None
        
        
        # Get metods
        def get_race(self):
            return self.race
            
        def get_gender(self):
            return self.gender
        
        # Set metods
        def set_race(self, race):
            if isinstance(race, RaceData):
                self.race = race
                return True
            
            return False
            
        def set_gender(self, gender):
            if isinstance(gender, RaceData):
                self.gender = gender
                return True
        
        return False