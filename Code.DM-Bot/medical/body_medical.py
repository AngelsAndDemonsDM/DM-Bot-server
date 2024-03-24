from .blood_system import BloodSystem
from .limb import LimbsSystem
from .need import Need
from organs.organs_system import OrgansSystem


class BodyMedical:
    def __init__(self):
        self.medical_stats = None # TODO
        
        self.blood_system = None
        self.limbs = None
        self.organs = None
        self.needs = None
