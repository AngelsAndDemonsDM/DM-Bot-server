class BodyMedical:
    def __init__(self) -> None:   
        # Organs
        # TODO

        # Stats
        self._body_stats = {
            "cognitive": self.cognitive,       # сознание
            "pain": self.pain,                 # боль
            "vision": self.vision,             # зрение
            "hearing": self.hearing,           # слух
            "scent": self.scent,               # обоняние
            "productivity": self.productivity, # работа
            "movement": self.movement,         # передвижение
            "fertility": self.fertility,       # фертильность
        }

        # Needs
        # TODO
        
    
    @property
    def cognitive(self):
        ...
    
    @property
    def pain(self):
        ...

    @property
    def vision(self):
        ...

    @property
    def hearing(self):
        ...

    @property
    def scent(self):
        ...

    @property
    def productivity(self):
        ...

    @property
    def movement(self):
        ...

    @property
    def fertility(self):
        ...
