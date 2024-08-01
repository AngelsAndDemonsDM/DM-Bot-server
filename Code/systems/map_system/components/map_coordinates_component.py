from typing import Any, Dict, List

from systems.entity_system import BaseComponent
from systems.map_system.coordinate import Coordinate

"""
Не объявляется в обычных прототипах
"""

class MapCoordinatesComponent(BaseComponent):
    __slots__ = ['coord_list']
    
    def __init__(self, coord_list: List[Coordinate] = None) -> None:
        super().__init__("MapCoordinatesComponent")
        self.coord_list: List[Coordinate] = coord_list

    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapCoordinatesComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapCoordinatesComponent(coord_list={self.coord_list})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента MapCoordinatesComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'coord_list': List[Coordinate]
        }
