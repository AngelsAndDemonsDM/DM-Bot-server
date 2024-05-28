from typing import Optional
from base_classes import Entity
from components.map import MapCoordinateComponent

class MapEntity(Entity):
    def __init__(self, entity_id: str, width: int, height: int):
        super().__init__(entity_id)
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def add_entity(self, entity: Entity, x: int, y: int):
        """Добавляет сущность на карту и устанавливает компонент координат."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = entity
            map_coord_component = MapCoordinateComponent(x, y)
            entity.add_component('MapCoordinateComponent', 'map_coord', map_coord_component)
        else:
            raise ValueError("Position out of bounds")

    def get_entity(self, x: int, y: int) -> Optional[Entity]:
        """Возвращает сущность по координатам."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise ValueError("Position out of bounds")

    def display(self) -> None:
        """Отображает карту в текстовом виде."""
        for row in self.grid:
            for cell in row:
                if cell is None:
                    print(".", end=" ")
                else:
                    print("E", end=" ")
            print()
