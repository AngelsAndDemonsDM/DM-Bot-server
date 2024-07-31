from typing import Dict, List

from systems.entity_system import BaseEntity
from systems.map_system.coordinate import Coordinate


class MapEntity(BaseEntity):
    __slots__ = ['map_objects']
    
    def __init__(self) -> None:
        super().__init__()
        self.map_objects: Dict[Coordinate, List[BaseEntity]] = {}
