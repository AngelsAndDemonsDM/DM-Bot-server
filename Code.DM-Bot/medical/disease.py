from effect import Effect


class Disease:
    def __init__(self) -> None:
        self._id: str
        self._name: str
        self._description: str
        self._effect: list[Effect]
        self._max_stage: int
        self._tick_per_stage: int

        self._cur_stage: int
        self._cur_tick: int
    
    def update(self):
        self._cur_tick += 1
        if self._cur_tick >= self._tick_per_stage:
            if self._cur_stage < self._max_stage:
                self._cur_stage += 1
            self._cur_tick = 0
