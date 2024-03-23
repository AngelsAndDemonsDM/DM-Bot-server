from medical.medical_enums import GenderEnum
from medical.organs.organ_base import OrganBase


class Genitalia(OrganBase):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, gender_type: GenderEnum):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._gender_type = gender_type

    def __str__(self):
        return f"{super().__str__()}; gender_type: {self._gender_type}"
