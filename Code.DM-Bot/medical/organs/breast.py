from medical.medical_enums import BreastSizeEnum
from medical.organs.organ_base import OrganBase


class Breast(OrganBase):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, size: BreastSizeEnum, reagent_per_day: int, reagent_per_tick: int, amount_reagent: int):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._size = size
        self._reagent_per_day = reagent_per_day
        self._reagent_per_tick = reagent_per_tick
        
        self._amount_reagent = amount_reagent

    def __str__(self):
        return f"{super().__str__()}; size: {self._size}; reagent_per_day: {self._reagent_per_day}; reagent_per_tick: {self._reagent_per_tick}; amount_reagent: {self._amount_reagent}"
