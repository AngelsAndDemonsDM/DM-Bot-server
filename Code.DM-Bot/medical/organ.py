from base_classes import BaseObject


class Organ(BaseObject):
    def __init__(self, id: str, name: str, description: str) -> None:
        super().__init__(id, name, description)
