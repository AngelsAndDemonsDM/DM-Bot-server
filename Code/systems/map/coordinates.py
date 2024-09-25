import math


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y

        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]

        return False

    def distance_to(self, other: "Coordinates") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return f"Coordinates(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"{self.x} {self.y}"

    @classmethod
    def from_str(cls, coord_str: str) -> "Coordinates":
        x, y = map(int, coord_str.split())
        return cls(x, y)
