from typing import Any, Dict

from systems.entity_system import BaseComponent

"""
  ...
  components:
    - type: MapPhysicsComponent
      invisibility_level: 0
      opaque: true
      passable: true
"""

class MapPhysicsComponent(BaseComponent):
    __slots__ = ['invisibility_level', 'opaque', 'passable']
    
    def __init__(self, invisibility_level: int, opaque: bool, passable: bool) -> None:
        """Инициализирует компонент MapPhysicsComponent с заданными параметрами.

        Args:
            invisibility_level (int): Уровень невидимости компонента.
            opaque (bool): Флаг, указывающий, является ли компонент непрозрачным.
            passable (bool): Флаг, указывающий, можно ли пройти через компонент.
        """
        super().__init__('MapPhysicsComponent')
        self.invisibility_level: int = invisibility_level
        self.opaque: bool = opaque
        self.passable: bool = passable
    
    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapPhysicsComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"MapPhysicsComponent(invisibility_level={self.invisibility_level}, opaque={self.opaque}, passable={self.passable})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента MapPhysicsComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'invisibility_level': int,
            'opaque': bool,
            'passable': bool
        }
