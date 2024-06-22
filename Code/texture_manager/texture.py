from typing import List


class Texture:
    __slots__ = []

    def __init__(self) -> None:
        self.path: str
        self.isCash: bool
        self.allow_state: List[str]
