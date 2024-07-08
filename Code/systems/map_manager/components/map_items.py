from typing import Any, Dict, List, Type, TypedDict

from systems.entity_system import BaseComponent

"""
- type: "MapEntity"
  id: "SomeValue"
  components:
    - type: MapItemsComponent
      items:
        - entity_id: "item1"
          entity_type: "type1"
          points:
            - {x: 0, y: 0}
            - {x: 1, y: 0}
        - entity_id: "item2"
          entity_type: "type2"
          points:
            - {x: 2, y: 2}
            - {x: 3, y: 3}
"""

class Point(TypedDict):
    x: int
    y: int

class Item(TypedDict):
    entity_id: str
    entity_type: str
    points: List[Point]

class MapItemsComponent(BaseComponent):
    __slots__ = ['items']
    
    def __init__(self, items: List[Item]) -> None:
        super().__init__('MapItemsComponent')
        self.items: List[Item] = items
    
    def __repr__(self) -> str:
        return f"MapItemsComponent(items={self.items})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Type[Any]]:
        return {'items': List[Item]}
