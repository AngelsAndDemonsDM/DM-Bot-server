from map_manager.map_manager import MapManager
from systems.entity_system import BaseEntity

"""
- type: "MapEntity"
  id: "SomeValue"
  components:
    ...
"""

class MapEntity(BaseEntity):
    __slots__ = []
    
    def __init__(self) -> None:
        super().__init__()
    
    def self_save(self, name: str) -> None:
        MapManager.save_map(self, name)
    
    def self_load(self, name: str) -> None:
        self = MapManager.load_map(name)