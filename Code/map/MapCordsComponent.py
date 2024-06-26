from factory.base_component import Component


class MapCordsComponent(Component):
    __slots__ = ['x', 'y', 'dimension']

    def __init__(self, x=0, y=0, dimension='null'):
        super().__init__()
        self.x = x
        self.y = y
        self.dimension = dimension

    def __repr__(self):
        return f"MapCordsComponent(x={self.x}, y={self.y}, dimension={self.dimension})"

    @classmethod
    def default_values(cls):
        return {'x': 0, 'y': 0, 'dimension': 'null'}
