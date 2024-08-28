import heapq
from copy import deepcopy
from typing import Dict, List

from DMBotTools import Coordinate, Shape
from systems.entity_system import BaseEntity, EntityFactory
from systems.map_system.components import *
from systems.map_system.components.map_physics_component import (
    MAP_PHYSICS_OBJ_TYPE, MapPhysicsObjType)


class MapColisionError(Exception):
    pass

class MapEntity(BaseEntity):
    __slots__ = ['basic_floor', 'map_floor_objects', 'map_main_objects', 'map_ceiling_objects', 'block_coodinates', 'move_queue']
    
    def __init__(self) -> None:
        super().__init__()
        self.basic_floor: BaseEntity = None # Базовый пол всей карты
        
        self.map_floor_objects:   Dict[Coordinate, List[BaseEntity]] = {} # Пол и разные загрязнения
        self.map_main_objects:    Dict[Coordinate, List[BaseEntity]] = {} # Основные объекты карты
        self.map_ceiling_objects: Dict[Coordinate, List[BaseEntity]] = {} # Потолок. Для просчёта корретного закрытых помещений и для гермитизации

        self.block_coodinates: List[Coordinate] # Лист координат которые заблокированы.
        
        self.move_queue: Dict[BaseEntity, List[Coordinate]] = {} # Очередь для движения. 

    @staticmethod
    def _get_shape_coordinates(obj: BaseEntity) -> List[Coordinate]:
        comp = obj.get_component('ShapeComponent')
        if comp:
            shape = comp.shape
        else:
            shape = Shape('x')
        
        return shape.get_list_coordinates()

    @staticmethod
    def _get_map_physics_component(obj: BaseEntity):
        comp = obj.get_component("MapPhysicsComponent")
        if not comp:
            comp = MapPhysicsComponent(False, MapPhysicsObjType.MAIN)
        
        return comp

    @staticmethod
    def _update_obj_coord(obj: BaseEntity, coordinates_to_update: List[Coordinate]):
        coordinate_comp = obj.get_component("MapCoordinatesComponent")
        if not coordinate_comp:
            coordinate_comp = MapCoordinatesComponent(deepcopy(coordinates_to_update))
            obj.add_component(coordinate_comp)
        
        else:
            coordinate_comp.coord_list = deepcopy(coordinates_to_update)

    def _remove_coodinates(self, obj: BaseEntity, obj_type: MAP_PHYSICS_OBJ_TYPE, list_to_remove: List[Coordinate], is_block: bool) -> None:
        # Удаляем объект с карты
        if obj_type == MapPhysicsObjType.CEILING:
            for coord in list_to_remove:
                if coord in self.map_ceiling_objects and self.map_ceiling_objects[coord] == obj:
                    del self.map_ceiling_objects[coord]

        elif obj_type == MapPhysicsObjType.MAIN:
            for coord in list_to_remove:
                if coord in self.map_main_objects and self.map_main_objects[coord] == obj:
                    del self.map_main_objects[coord]

        else:
            for coord in list_to_remove:
                if coord in self.map_floor_objects and self.map_floor_objects[coord] == obj:
                    del self.map_floor_objects[coord]

        # Разблокируем координаты
        if is_block:
            for coord in list_to_remove:
                if coord in self.block_coodinates:
                    self.block_coodinates.remove(coord)
    
    def add_object_by_uid(self, uid: int, source_coordinate: Coordinate) -> None:
        ent_factory = EntityFactory()
        obj = ent_factory.get_entity_by_uid(uid)
        if not obj:
            raise ValueError(f"Entity {uid} don't exist")
        
        self.add_object(obj, source_coordinate)
    
    def add_object(self, obj: BaseEntity, source_coordinate: Coordinate) -> None:
        obj_shape_coodinates = MapEntity._get_shape_coordinates(obj)
        obj_physics_comp = MapEntity._get_map_physics_component(obj)
        obj_type = obj_physics_comp.obj_type
        
        # Создаём список куда пихать обьект
        coordinates_to_add: List[Coordinate] = []
        for coordinate in obj_shape_coodinates:
            coordinates_to_add.append(source_coordinate + coordinate)
        
        # Проверяем что можем засунуть объект
        for coordinate in coordinates_to_add:
            if coordinate in self.block_coodinates:
                raise MapColisionError()
        
        # Пихаем ~~чле~~ объект в массив
        if obj_type == MapPhysicsObjType.CEILING:
            for coord in coordinates_to_add:
                self.map_ceiling_objects[coord] = obj
        
        elif obj_type == MapPhysicsObjType.MAIN:
            for coord in coordinates_to_add:
                self.map_main_objects[coord] = obj
        
        else:
            for coord in coordinates_to_add:
                self.map_floor_objects[coord] = obj
        
        # Блокируем координаты
        if obj_physics_comp.block_coordinate:
            self.block_coodinates.extend(coordinates_to_add)
        
        # Устанавливаем координаты в объект
        self._update_obj_coord(obj, coordinates_to_add)
    
    def remove_object_uid(self, uid: int) -> None:
        ent_factory = EntityFactory()
        obj = ent_factory.get_entity_by_uid(uid)
        if not obj:
            return
        
        self.remove_object(obj)

    def remove_object(self, obj: BaseEntity) -> None:
        coordinates_to_remove = obj.get_component("MapCoordinatesComponent")
        if not coordinates_to_remove:
            return
        
        obj_physics_comp = MapEntity._get_map_physics_component(obj)

        self._remove_coodinates(obj, obj_physics_comp.obj_type, coordinates_to_remove.coord_list, obj_physics_comp.block_coordinate)

        obj.remove_component("MapCoordinatesComponent")
    
    def do_step(self) -> None:
        for obj, path in list(self.move_queue.items()):
            if path:
                next_coordinate = path.pop(0)
                self.teleport_object(obj, next_coordinate)
                if not path:
                    del self.move_queue[obj]
    
    def teleport_object_by_uid(self, uid: int, target_coordinate: Coordinate) -> None:
        ent_factory = EntityFactory()
        obj = ent_factory.get_entity_by_uid(uid)
        if not obj:
            return
        
        self.add_object(obj, target_coordinate)
        self.remove_object(obj)
    
    def teleport_object(self, obj: BaseEntity, target_coordinate: Coordinate) -> None:
        self.add_object(obj, target_coordinate)
        self.remove_object(obj)
        
    def move_object_by_uid(self, uid: int, target_coordinate: Coordinate) -> None:
        ent_factory = EntityFactory()
        obj = ent_factory.get_entity_by_uid(uid)
        if not obj:
            return
        
        self.move_object(obj, target_coordinate)
    
    def move_object(self, obj: BaseEntity, target_coordinate: Coordinate) -> None:
        current_coordinates = obj.get_component("MapCoordinatesComponent").coord_list
        if not current_coordinates:
            return
        
        start_coordinate = current_coordinates[0]
        path = a_star_search(start_coordinate, target_coordinate, self.block_coodinates)
        
        if path:
            self.move_queue[obj] = path
    
    @staticmethod
    def _get_coordinates_in_radius(origin: Coordinate, radius: int) -> List[Coordinate]:
        coordinates_in_radius = []
        for x in range(origin.x - radius, origin.x + radius + 1):
            for y in range(origin.y - radius, origin.y + radius + 1):
                candidate = Coordinate(x, y)
                if Coordinate.distance(origin, candidate) <= radius:
                    coordinates_in_radius.append(candidate)
        
        return coordinates_in_radius

    def get_entitys_in_range(self, origin: Coordinate, radius: int) -> List[BaseEntity]:
        entities_in_range = []
        coordinates_in_radius = self._get_coordinates_in_radius(origin, radius)

        for coord in coordinates_in_radius:
            if coord in self.map_floor_objects:
                entities_in_range.extend(self.map_floor_objects[coord])
        
            if coord in self.map_main_objects:
                entities_in_range.extend(self.map_main_objects[coord])
        
            if coord in self.map_ceiling_objects:
                entities_in_range.extend(self.map_ceiling_objects[coord])
        
        return entities_in_range

def get_neighbors(coord: Coordinate) -> List[Coordinate]:
    return [
        Coordinate(coord.x + 1, coord.y),
        Coordinate(coord.x - 1, coord.y),
        Coordinate(coord.x, coord.y + 1),
        Coordinate(coord.x, coord.y - 1),
        Coordinate(coord.x + 1, coord.y + 1),
        Coordinate(coord.x - 1, coord.y - 1),
        Coordinate(coord.x + 1, coord.y - 1),
        Coordinate(coord.x - 1, coord.y + 1),
    ]

def a_star_search(start: Coordinate, goal: Coordinate, blocked_coords: List[Coordinate]) -> List[Coordinate]:
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: Coordinate.distance(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            if neighbor in blocked_coords:
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + Coordinate.distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []
