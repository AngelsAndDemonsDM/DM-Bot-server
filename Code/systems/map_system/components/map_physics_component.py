from enum import Enum
from typing import Any, Dict, Literal

from systems.entity_system import BaseComponent

"""
  ...
  components:
    - type: MapPhysicsComponent
      block_coordinate: True / False
      obj_type: 0 / 1 / 2 # 2 - ceiling / 1 - main / 0 - floor
"""

class MapPhysicsObjType(Enum):
    FLOOR   = 0
    MAIN    = 1
    CEILING = 2

MAP_PHYSICS_OBJ_TYPE = Literal[MapPhysicsObjType.FLOOR, MapPhysicsObjType.MAIN, MapPhysicsObjType.CEILING]

class MapPhysicsComponent(BaseComponent):
    __slots__ = ['block_coordinate', '_obj_type']
    
    def __init__(self, block_coordinare: bool, obj_type: int) -> None:
        super().__init__("MapPhysicsComponent")
        self.block_coordinate: bool = block_coordinare
        self._obj_type: MAP_PHYSICS_OBJ_TYPE = MapPhysicsComponent._validate_map_obj(obj_type) # Одно из сделующих. 2 - ceiling / 1 - main / 0 - floor

    @property
    def obj_type(self) -> MAP_PHYSICS_OBJ_TYPE:
        return self._obj_type
    
    @obj_type.setter
    def obj_type(self, value: int) -> None:
        self._obj_type = MapPhysicsComponent._validate_map_obj(value)
    
    @staticmethod
    def _validate_map_obj(value: int) -> MAP_PHYSICS_OBJ_TYPE:
        """Проверяет, что значение находится в диапазоне от 0 до 2 включительно и возвращает соответствующий элемент перечисления.

        Args:
            value (int): Значение для проверки.

        Raises:
            ValueError: Если значение не находится в диапазоне от 0 до 2.

        Returns:
            MAP_PHYSICS_OBJ_TYPE: Проверенное значение как элемент перечисления.
        """
        if value < 0 or value > 2:
            raise ValueError(f"MapPhysicsComponent can have obj_type only 0, 1, or 2. Value on init: '{value}'")
        
        return MapPhysicsObjType(value)

    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapPhysicsComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapPhysicsComponent(shape={self.shape!r})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента MapPhysicsComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'block_coordinare': bool,
            'obj_type': int
        }