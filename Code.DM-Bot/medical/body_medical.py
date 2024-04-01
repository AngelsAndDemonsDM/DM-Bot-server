class BodyMedical:
    def __init__(self) -> None:   
        # Organs
        # TODO

        # Stats
        self._body_stats = {
            "consciousness": self.consciousness, #сознание
            "pain": self.pain, # боль
            "vision": self.vision, # зрение
            "hearing": self.hearing, # слух
            "sense_of_smell": self.sense_of_smell, # обоняние
            "job": self.job, # работа
            "movement": self.movement, # передвижение
            "fertility": self.consciousness, # фертильность
        }
    
    @property
    def consciousness(self):
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
    def sense_of_smell(self):
        ...

    @property
    def job(self):
        ...

    @property
    def movement(self):
        ...

    @property
    def fertility(self):
        ...