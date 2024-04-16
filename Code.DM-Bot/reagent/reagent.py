from .reagent_state.base_reagent_state import BaseReagentState
from .reagent_state.reagent_enum import ReagentEnum
from etc.base_classes import BaseObject

class Reagent(BaseObject):
    def __init__(self, id: str, name: str, description: str, boiling_temp: float, crystal_temp: float, temp: float, action: list[BaseReagentState] = None) -> None:
        super().__init__(id, name, description)
        
        self._boiling_temp = boiling_temp
        self._crystal_temp = crystal_temp
        self._temp = temp
        self._state = None

        self._action: list[BaseReagentState] = action if action is not None else [] 
        self.update_state()

    # Get metods
    @property
    def boiling_temp(self) -> float:
        return self._boiling_temp

    @property
    def crystal_temp(self) -> float:
        return self._crystal_temp

    @property
    def state(self) -> ReagentEnum:
        return self._state

    # Class metods
    def delta_temp(self, value: float) -> None:
        self._temp += value

    def update_state(self) -> None:
        if self._temp > self._boiling_temp:
            self._current_state = ReagentEnum.GAS
        elif self._temp < self._crystal_temp:
            self._current_state = ReagentEnum.SOLID
        else:
            self._current_state = ReagentEnum.LIQUID
        