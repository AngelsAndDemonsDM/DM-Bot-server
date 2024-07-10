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
        super().__init__('MapPhysicsComponent')
        self.invisibility_level: int = invisibility_level
        self.opaque: bool = opaque
        self.passable: bool = passable
    
    def __repr__(self) -> str:
        return f"MapPhysicsComponent(invisibility_level={self.invisibility_level}, opaque={self.opaque}, passable={self.passable})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        return {
            'invisibility_level': int,
            'opaque': bool,
            'passable': bool
        }
