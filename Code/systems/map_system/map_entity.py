from typing import Dict, List

from systems.entity_system import BaseEntity
from systems.map_system.coordinate import Coordinate
from systems.map_system.shape import Shape


class MapCoordConflictError(Exception):
    def __init__(self, message: str, coordinates: List['Coordinate']):
        super().__init__(message)
        self.coordinates = coordinates

class MapEntity(BaseEntity):
    __slots__ = ['map_objects']
    
    def __init__(self) -> None:
        super().__init__(0)
        self.map_objects: Dict[Coordinate, BaseEntity] = {}

    def add_object(self, obj: BaseEntity, coordinate: Coordinate) -> None:
        shape = obj.get_component("ShapeComponent")
        if not shape:
            shape = Shape('x')
        
        for coord in shape.get_list_coordinates():
            new_coord = coordinate + coord
            self.map_objects[new_coord] = obj
    
    def find_coordinates(self, uid: int) -> List[Coordinate]:
        return [coord for coord, entity in self.map_objects.items() if entity.uid == uid]
    
    def remove_object(self, uid: int) -> None:
        coordinates_to_remove = self.find_coordinates(uid)
        self._remove_coordinates(coordinates_to_remove)
    
    def _remove_coordinates(self, coordinates: List[Coordinate]) -> None:
        for coord in coordinates:
            del self.map_objects[coord]

    def move_object(self, uid: int, delta: Coordinate, allow_replace: bool = True) -> None:
        current_coords = self.find_coordinates(uid)
        if not current_coords:
            return
        
        obj = self.map_objects[current_coords[0]]

        conflict_coords = []
        new_coords = []
        for coord in current_coords:
            new_coord = coord + delta
            if new_coord in self.map_objects:
                conflict_coords.append(new_coord)
                if not allow_replace:
                    raise MapCoordConflictError(f"Conflict at {new_coord}", conflict_coords)
            new_coords.append(new_coord)
        
        self._remove_coordinates(current_coords)
        for new_coord in new_coords:
            self.map_objects[new_coord] = obj

    def teleport_object(self, uid: int, new_base_coordinate: Coordinate, allow_replace: bool = True) -> None:
        current_coords = self.find_coordinates(uid)
        if not current_coords:
            return
        
        obj = self.map_objects[current_coords[0]]

        shape = obj.get_component("ShapeComponent")
        if not shape:
            shape = Shape('x')
        
        conflict_coords = []
        new_coords = []
        for coord in shape.get_list_coordinates():
            new_coord = new_base_coordinate + coord
            if new_coord in self.map_objects:
                conflict_coords.append(new_coord)
                if not allow_replace:
                    raise MapCoordConflictError(f"Conflict at {new_coord}", conflict_coords)
            
            new_coords.append(new_coord)
        
        self._remove_coordinates(current_coords)
        for new_coord in new_coords:
            self.map_objects[new_coord] = obj
