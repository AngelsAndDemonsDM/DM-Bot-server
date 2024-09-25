from typing import Any, Dict

from systems.ecs import BaseComponent, register_component
from systems.map.coordinate import Coordinate


@register_component
class CoordinateComponent(BaseComponent):
    def __init__(self, coordinate: Coordinate) -> None:
        super().__init__()
        self.coord: Coordinate = coordinate

    def dump(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "coordinate": str(self.coord),
        }

    @classmethod
    def restore(cls, data: Dict[str, Any]) -> "CoordinateComponent":
        coord_str = data.get("coordinate", "0 0")
        coord = Coordinate.from_str(coord_str)

        return cls(coord)
