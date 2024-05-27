from effect import Effect

from .base_reagent_state import BaseReagentState


class SolidReagentState(BaseReagentState):
    def __init__(self, reagent_id: str, nutrient: int, hydration: int, effects: list[Effect]) -> None:
        super().__init__(reagent_id, nutrient, hydration, effects)
