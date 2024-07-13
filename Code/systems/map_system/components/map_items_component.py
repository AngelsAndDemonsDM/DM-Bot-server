import logging
from typing import Any, Dict, List, Type, TypedDict

from systems.entity_system import BaseComponent, EntityFactory
from systems.map_system.components.map_coordinates_component import \
    MapCoordinateComponent
from systems.map_system.coordinates import Coordinate

"""
  ...
  components:
    - type: MapItemsComponent
      items:
        - entity_id: "item1"
          entity_type: "type1"
          coordinates:
            - {x: 0, y: 0}
            - {x: 1, y: 0}
        - entity_id: "item2"
          entity_type: "type2"
          coordinates:
            - {x: 2, y: 2}
            - {x: 3, y: 3}
        ...
"""

class Item(TypedDict):
    """Класс для представления элемента на карте.

    Attributes:
        entity_id (str): Идентификатор элемента.
        entity_type (str): Тип элемента.
        coordinates (List[Coordinate]): Список координат, на которых находится элемент.
    """
    entity_id: str
    entity_type: str
    coordinates: List[Coordinate]

class MapItemsComponent(BaseComponent):
    __slots__ = ['items', 'objects']
    
    def __init__(self, items: List[Item]) -> None:
        """Инициализирует компонент MapItemsComponent с заданным списком элементов.

        Args:
            items (List[Item]): Список элементов, содержащих идентификатор, тип и координаты.
        """
        super().__init__('MapItemsComponent')
        self.items: List[Item] = items
        self.objects: List['BaseEntity'] = [] # type: ignore
    
    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapItemsComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapItemsComponent(items={self.items}, objects={self.objects})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Type[Any]]:
        """Возвращает словарь с именами переменных и их типами для компонента MapItemsComponent.

        Returns:
            Dict[str, Type[Any]]: Словарь с именами переменных и их типами.
        """
        return {
            'items': List[Item]
        }

    def setup_objects(self, entity_factory: EntityFactory) -> None:
        if not self.items:
            return

        for item in self.items:
            obj = entity_factory.get_entity_by_id(item['entity_type'], item['entity_id'])

            if not obj:
                logging.warning(f"Entity ID: {item['entity_id']}, entity type: {item['entity_type']} is not a valid entity object")
                continue

            self.objects.append(obj)
            obj.add_component(MapCoordinateComponent(self.owner, item['coordinates']))

        self.items.clear()
