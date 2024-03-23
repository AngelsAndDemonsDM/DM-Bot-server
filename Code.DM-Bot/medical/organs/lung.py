from medical.organs.organ_base import OrganBase


class Lung(OrganBase):
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str):
        super().__init__(id, name, description, max_health, standart_efficiency, subtype)
        
    def __str__(self):
        return f"{super().__str__()};"
