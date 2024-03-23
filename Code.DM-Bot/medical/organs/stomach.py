from medical.organs.organ_base import OrganBase


class Stomach(OrganBase):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str, volume: float):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        self._volume = volume

    def __str__(self):
        return f"{super().__str__()}; volume: {self._volume}"
