from base_classes import Component


class MapCoordinateComponent(Component):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def update(self):
        pass
