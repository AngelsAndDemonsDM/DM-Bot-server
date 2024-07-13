from typing import Any, Dict, List

from systems.entity_system import BaseEntity
from systems.entity_system.factory import EntityFactory
from systems.map_system.components.map_coordinates_component import \
    MapCoordinateComponent
from systems.map_system.components.map_items_component import MapItemsComponent
from systems.map_system.components.map_physics_component import \
    MapPhysicsComponent
from systems.map_system.coordinates import Coordinate
from systems.map_system.map_manager import MapManager

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
        
        def is_visible(observer_pos: Coordinate, target_pos: Coordinate, blocking_objects: List[Dict[str, Any]]) -> bool:
            # Проверка видимости с учетом блокировки непрозрачными объектами
            x0, y0 = observer_pos.x, observer_pos.y
            x1, y1 = target_pos.x, target_pos.y
            dx, dy = x1 - x0, y1 - y0
            distance = Coordinate.distance(observer_pos, target_pos)
            steps = int(distance)
            if steps == 0:
                return True

            x_increment = dx / steps
            y_increment = dy / steps

            x, y = x0, y0
            for _ in range(steps):
                x += x_increment
                y += y_increment
                current_pos = Coordinate(int(round(x)), int(round(y)))
                for blocking_obj in blocking_objects:
                    if current_pos in blocking_obj['coordinates']:
                        return False
            return True

        # Сначала собираем все блокирующие объекты
        blocking_objects = []
        for obj in map_items_component.objects:
            coordinates_component: MapCoordinateComponent = obj.get_component("MapCoordinateComponent")
            if not coordinates_component:
                continue

            physics_component: MapPhysicsComponent = obj.get_component("MapPhysicsComponent")
            if not physics_component:
                physics_component = MapPhysicsComponent(0, True, True)
            
            if physics_component.opaque:
                blocking_objects.append({'coordinates': coordinates_component.coordinates})

        # Проверяем видимость всех объектов
        for obj in map_items_component.objects:
            item_visible = False
            
            coordinates_component: MapCoordinateComponent = obj.get_component("MapCoordinateComponent")
            if not coordinates_component:
                continue
            
            physics_component: MapPhysicsComponent = obj.get_component("MapPhysicsComponent")
            if not physics_component:
                physics_component = MapPhysicsComponent(0, True, True)
            
            if physics_component.invisibility_level > detection_level:
                continue  # Пропускаем предмет, если уровень невидимости выше уровня обнаружения
                
            for coord in coordinates_component.coordinates:
                if Coordinate.distance(position, coord) <= visibility_range:
                    if is_visible(position, coord, blocking_objects):
                        item_visible = True
                        break
        
            if item_visible:
                visible_items.append({'entity': obj, 'coordinates': coordinates_component.coordinates})

        return visible_items
