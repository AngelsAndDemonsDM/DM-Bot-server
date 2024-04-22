from etc import Effect

from .base_medical_class import BaseMedicalClass


class Implant(BaseMedicalClass):
    def __init__(self, id: str, name: str, description: str, base_effect: Effect, base_efficiency: float, max_hp: float, cur_hp: float) -> None:
        super().__init__(id, name, description, base_effect, base_efficiency, max_hp, cur_hp)
