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
        """Инициализирует сущность карты."""
        super().__init__()
    
    def self_save(self, name: str, entity_factory: EntityFactory) -> None:
        """Сохраняет текущее состояние карты.

        Args:
            name (str): Имя файла, в который будет сохранена карта.
            entity_factory (EntityFactory): Фабрика сущностей для создания объектов.
        """
        comp: MapItemsComponent = self.get_component("MapItemsComponent")
        comp.setup_objects(entity_factory)
        MapManager.save_map(self, name)
    
    def self_load(self, name: str) -> None:
        """Загружает состояние карты из файла.

        Args:
            name (str): Имя файла, из которого будет загружена карта.
        """
        self = MapManager.load_map(name)

    def calculate_visibility_area(
        self, 
        position: Coordinate, 
        detection_level: int, 
        visibility_range: int, 
        entity_factory: EntityFactory
    ) -> List[Dict[str, Any]]:
        """Вычисляет область видимости с заданной позиции.

        Args:
            position (Coordinate): Позиция наблюдателя на карте.
            detection_level (int): Уровень обнаружения.
            visibility_range (int): Дальность видимости.
            entity_factory (EntityFactory): Фабрика сущностей для создания объектов.

        Returns:
            List[Dict[str, Any]]: Список видимых предметов, включая их координаты и другие свойства.
        """
        map_items_component: MapItemsComponent = self.get_component("MapItemsComponent")
        if not map_items_component:
            return []

        map_items_component.setup_objects(entity_factory)
        
        visible_items: List[Dict[str, Any]] = []

        for obj in map_items_component.objects:
            for entity, coordinates in obj.items():
                item_visible = False
                physics_component: MapPhysicsComponent = entity.get_component("MapPhysicsComponent")
                
                if physics_component:
                    if physics_component.invisibility_level > detection_level:
                        continue  # пропускаем предмет, если уровень невидимости выше уровня обнаружения
                    
                    if physics_component.opaque:
                        for coord in coordinates:
                            distance = Coordinate.distance(position, coord)
                            if distance <= visibility_range:
                                item_visible = True
                                break  # если предмет видим, добавляем его и выходим из цикла по точкам

                if item_visible:
                    visible_items.append({'entity': entity, 'coordinates': coordinates})

        return visible_items
