from copy import deepcopy

from effect import Effect


class BaseReagentState:
    def __init__(self, reagent_id:str, nutrient: int, hydration: int, effects: list[Effect]) -> None:
        self._reagent_id = reagent_id
        self._nutrient = nutrient
        self._hydration = hydration
        self._effects = deepcopy(effects)
    
    @property
    def reagent_id(self) -> str:
        return self._reagent_id

    @property
    def nutrient(self) -> int:
        return self._nutrient
    
    @property
    def hydration(self) -> int:
        return self._hydration
    
    @property
    def effects(self) -> list[Effect]:
        return self._effects
    
    @reagent_id.setter
    def reagent_id(self, value: str) -> None:
        self._reagent_id = value

    @nutrient.setter
    def nutruent(self, value: int) -> None:
        self._nutrient = value
    
    @hydration.setter
    def hydration(self, value: int) -> None:
        self._hydration = value
    
    @effects.setter
    def effects(self, value: list[Effect]) -> None:
        self._effects = deepcopy(value)
