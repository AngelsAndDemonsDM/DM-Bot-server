from base_classes.base_object import BaseObject
from etc.effect import Effect


class Disease(BaseObject):
    def __init__(self, id: str, name: str, description: str) -> None:
        super().__init__(id, name, description)
        self._effect: list[Effect]
        self._max_stage: int
        self._tick_per_stage: int

        self._cur_stage: int
        self._cur_tick: int
    
    # Get metods
    @property
    def effect(self) -> list[Effect]:
        return self._effect

    def update(self):
        self._cur_tick += 1
        if self._cur_tick >= self._tick_per_stage:
            if self._cur_stage < self._max_stage:
                self._cur_stage += 1
            self._cur_tick = 0
