from copy import deepcopy
from typing import Dict, List

from systems.entity_system import BaseEntity, EntityFactory
from systems.map_system.components import *
from systems.map_system.components.map_physics_component import \
    MapPhysicsObjType, MAP_PHYSICS_OBJ_TYPE
from systems.map_system.coordinate import Coordinate
from systems.map_system.shape import Shape


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

    def remove_coodinates(self, obj: BaseEntity, obj_type: MAP_PHYSICS_OBJ_TYPE, list_to_remove: List[Coordinate], is_block: bool) -> None:
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

        self.remove_coodinates(obj, obj_physics_comp.obj_type, coordinates_to_remove.coord_list, obj_physics_comp.block_coordinate)

        obj.remove_component("MapCoordinatesComponent")
    
    def do_step(self) -> None:
        pass
    
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
        
    
    def move_object(self, uid: int, target_coordinate: Coordinate) -> None:
        pass