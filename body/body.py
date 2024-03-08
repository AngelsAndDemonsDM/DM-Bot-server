from race.race_data import RaceData

class Body:
    def __init__(self, race = None):
        self.race = None 
        if race != None:
            if not self.set_race(race):
                raise ValueError("Failed to set race in Body.")
        
        self.specialization = None # TODO
        self.stats = None # TODO
        
        self.body_effects = None # TODO
        self.body_items = None # TODO
        self.body_medical = None # TODO
        
        # Get metods
        def get_race(self):
            return self.race
        
        # Set metods
        def set_race(self, race):
            if isinstance(race, RaceData):
                self.race = race
                return True
            
            return False