from base_classes.base_object import BaseObject


class Implant(BaseObject):
    def __init__(self, id: str, name: str, description: str) -> None:
        super().__init__(id, name, description)
