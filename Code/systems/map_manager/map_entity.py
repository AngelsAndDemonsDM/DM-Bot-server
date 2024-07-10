from typing import Any, Dict, List

from map_manager.map_manager import MapManager
from systems.entity_system import BaseEntity
from systems.entity_system.factory import EntityFactory
from systems.map_manager.components.map_items_component import \
    MapItemsComponent
from systems.map_manager.components.map_physics_component import \
    MapPhysicsComponent
from systems.map_manager.coordinates import Coordinate

"""
- type: "MapEntity"
  id: "SomeValue"
  components:
    ...
"""

class MapEntity(BaseEntity):
    __slots__ = []
    
    def __init__(self) -> None:
        super().__init__()
    
    def self_save(self, name: str) -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        MapManager.save_map(self, name)
    
    def self_load(self, name: str) -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        self = MapManager.load_map(name)

    def calculate_visibility_area(
        self, 
        position: Coordinate, 
        detection_level: int, 
        visibility_range: int, 
        entity_factory: EntityFactory
    ) -> List[Dict[str, Any]]:
        """_summary_

        Args:
            position (Coordinate): _description_
            detection_level (int): _description_
            visibility_range (int): _description_
            entity_factory (EntityFactory): _description_

        Returns:
            List[Dict[str, Any]]: _description_
        """
        map_items_component: MapItemsComponent = self.get_component("MapItemsComponent")
        if not map_items_component:
            return []

        visible_items = []

        for item in map_items_component.items:
            item_visible = False
            entity: BaseEntity = entity_factory(item['entity_type'], item['entity_id'])
            if not entity:
                continue
            
            physics_component: MapPhysicsComponent = entity.get_component("MapPhysicsComponent")
            
            if physics_component:
                if physics_component.invisibility_level > detection_level:
                    continue  # пропускаем предмет, если уровень невидимости выше уровня обнаружения
                
                if physics_component.opaque:
                    for coord in item['coordinates']:
                        distance = abs(coord['x'] - position['x']) + abs(coord['y'] - position['y'])
                        if distance <= visibility_range:
                            item_visible = True
                            break  # если предмет видим, добавляем его и выходим из цикла по точкам

            if item_visible:
                visible_items.append(item)

        return visible_items
