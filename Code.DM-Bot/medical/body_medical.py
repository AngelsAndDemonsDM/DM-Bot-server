from .blood_system import BloodSystem
from .limb import LimbsSystem
from .need import Need
from .organ import OrgansSystem


class BodyMedical:
    def __init__(self):
        self.medical_stats = None # TODO
        
        self.blood_system = None
        self.limbs = None
        self.organs = None
        self.needs = None

class Organ:
    def __init__(self, name="", description="", health=100, maxhealth=100, standard_efficiency=100):
        self.name = name
        self.description = description
        self.health = health
        self.maxhealth = maxhealth
        self.standard_efficiency = standard_efficiency

    def getname(self):
        return self.name

    def setname(self, value):
        self.name = value

    def getdescription(self):
        return self.description

    def setdescription(self, value):
        self.description = value

    def gethealth(self):
        return self.health

    def getmaxhealth(self):
        return self.maxhealth

    def getstandard_efficiency(self):
        return self.standard_efficiency

    def sethealth(self, value):
        """
        Установить текущее здоровье органа.

        Args:
            value (int): Новое значение здоровья органа.
        """
        if value < 0:
            self.health = 0
        elif value > self.maxhealth:
            self.health = self.maxhealth
        else:
            self.health = value

    def setstandard_efficiency(self, value):
        self.standard_efficiency = value

    def setmaxhealth(self, value):
        self.maxhealth = value
