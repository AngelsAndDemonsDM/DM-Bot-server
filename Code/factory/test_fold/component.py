from Code.factory import Component


class HealthComponent(Component):
    __slots__ = ['health']

    def __init__(self, health=100):
        super().__init__()
        self.health = health

    def __repr__(self):
        return f"HealthComponent(health={self.health})"

    @classmethod
    def default_values(cls):
        return {'health': 100}

class PositionComponent(Component):
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PositionComponent(x={self.x}, y={self.y})"

    @classmethod
    def default_values(cls):
        return {'x': 0, 'y': 0}
