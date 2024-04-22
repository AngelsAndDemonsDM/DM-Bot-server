from base_classes import BaseObject
from etc import Effect


class BaseMedicalClass(BaseObject):
    def __init__(self, id: str, name: str, description: str, base_effect: Effect, base_efficiency: float, max_hp: float, cur_hp: float) -> None:
        super().__init__(id, name, description)
        self._base_effect: Effect = base_effect
        self._base_efficiency: float = base_efficiency

        self._max_hp: float = max_hp
        self._cur_hp: float = cur_hp
    
    # Get metods
    @property
    def base_effect(self) -> Effect:
        return self._base_effect

    @property
    def base_efficiency(self) -> float:
        return self._base_efficiency

    @property
    def max_hp(self) -> float:
        return self._max_hp

    @property
    def hp(self) -> float:
        return self._cur_hp

    # Set metods
    @base_effect.setter
    def base_effect(self, value: Effect) -> None:
        self._base_effect = value

    @base_efficiency.setter
    def base_efficiency(self, value: float) -> None:
        self._base_efficiency = value

    @max_hp.setter
    def max_hp(self, value: float) -> None:
        self._max_hp = value