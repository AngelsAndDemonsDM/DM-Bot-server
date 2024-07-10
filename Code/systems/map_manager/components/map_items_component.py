from typing import Any, Dict, List, Type, TypedDict

from systems.entity_system import BaseComponent
from systems.map_manager.coordinates import Coordinate

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
    __slots__ = ['items']
    
    def __init__(self, items: List[Item]) -> None:
        """Инициализирует компонент MapItemsComponent с заданным списком элементов.

        Args:
            items (List[Item]): Список элементов, содержащих идентификатор, тип и координаты.
        """
        super().__init__('MapItemsComponent')
        self.items: List[Item] = items
    
    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapItemsComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapItemsComponent(items={self.items})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Type[Any]]:
        """Возвращает словарь с именами переменных и их типами для компонента MapItemsComponent.

        Returns:
            Dict[str, Type[Any]]: Словарь с именами переменных и их типами.
        """
        return {
            'items': List[Item]
        }
