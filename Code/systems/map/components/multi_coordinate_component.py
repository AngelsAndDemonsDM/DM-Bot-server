from typing import Any, Dict, List, Optional

from systems.ecs import BaseComponent, register_component
from systems.map.coordinate import Coordinate


@register_component
class MultiCoordinateComponent(BaseComponent):
    def __init__(self, coordinates: Optional[Coordinate | List[Coordinate]] = None, mapuid: int = 0) -> None:
        super().__init__()
        
        self.mapuid: int = 0

        if coordinates is None:
            coordinates = []

        if not isinstance(coordinates, list):
            coordinates = [coordinates]

        self._coordinates: List[Coordinate] = coordinates

    @property
    def coordinates(self) -> List[Coordinate]:
        return self._coordinates

    def remove_coordinate(self, coordinates: Coordinate | List[Coordinate]) -> None:
        if not isinstance(coordinates, list):
            coordinates = [coordinates]

        for coord in coordinates:
            if coord in self._coordinates:
                self._coordinates.remove(coord)

    def add_coordinate(self, coordinate: Coordinate | List[Coordinate]) -> None:
        if not isinstance(coordinate, list):
            coordinate = [coordinate]

        for coord in coordinate:
            if coord not in self._coordinates:
                self._coordinates.append(coord)

        self._coordinates.sort()

    def dump(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "coordinates": [str(coord) for coord in self._coordinates],
        }

    @classmethod
    def restore(cls, data: Dict[str, Any]) -> "MultiCoordinateComponent":
        coord_str_l = data.get("coordinates", [])

        coord_l = []
        for coord_str in coord_str_l:
            coord_l.append(Coordinate.from_str(coord_str))

        return cls(coord_l)
