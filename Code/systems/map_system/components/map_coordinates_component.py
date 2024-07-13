from typing import Any, Dict, List

from systems.entity_system import BaseComponent
from systems.map_system.coordinates import Coordinate

"""
  ...
  components:
    - type: MapCoordinateComponent
      map_id: SomeMapId
      coordinates:
        - {x: 1, y: 0}
        - {x: 2, y: 0}
        ...
"""

class MapCoordinateComponent(BaseComponent):
    __slots__ = ['map_id', 'coordinates']
    
    def __init__(self, map_id: str, coordinates: List[Coordinate]) -> None:
        super().__init__('MapCoordinateComponent')
        self.map_id = map_id
        self.coordinates = coordinates
    
    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapCoordinateComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapCoordinateComponent(map_id={self.map_id}, coordinates={self.coordinates})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента MapCoordinateComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'map_id': str,
            'coordinates': List[Coordinate]
        }
