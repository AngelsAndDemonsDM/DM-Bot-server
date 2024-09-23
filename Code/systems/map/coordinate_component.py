from typing import Any, Dict
from systems.ecs import BaseComponent, register_component


@register_component
class CoordinateComponent(BaseComponent):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__()

        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def dump(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "x": self._x,
            "y": self._y,
        }

    @classmethod
    def restore(cls, data: Dict[str, Any]) -> "CoordinateComponent":
        x = data.get("x", 0)
        y = data.get("y", 0)

        return cls(x=x, y=y)
