from typing import Any, Dict, List, Optional

from systems.ecs import BaseEntity, Factory

from .coordinates import Coordinates


class MapEntity(BaseEntity):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.entities: Dict[Coordinates, List[BaseEntity]] = {}

    def add_entity_coords(self, x: int, y: int, entity: BaseEntity) -> None:
        """Добавляем сущность на карту по координатам (x, y)"""
        coords = Coordinates(x, y)
        self.add_entity(coords, entity)

    def add_entity(self, coords: Coordinates, entity: BaseEntity) -> None:
        """Добавляем сущность на карту по координатам"""
        if coords not in self.entities:
            self.entities[coords] = []

        self.entities[coords].append(entity)

    def get_entities(self, x: int, y: int) -> Optional[List[BaseEntity]]:
        coords = Coordinates(x, y)
        return self.entities.get(coords, None)

    def remove_entity_coords(self, x: int, y: int, entity: BaseEntity) -> None:
        coords = Coordinates(x, y)
        self.remove_entity(coords, entity)

    def remove_entity(self, coords: Coordinates, entity: BaseEntity) -> None:
        if coords in self.entities:
            if entity in self.entities[coords]:
                self.entities[coords].remove(entity)

            if not self.entities[coords]:
                del self.entities[coords]

    def get_entities_in_radius_coord(
        self, x: int, y: int, radius: float
    ) -> List[BaseEntity]:
        center = Coordinates(x, y)
        return self.get_entities_in_radius(center, radius)

    def get_entities_in_radius(
        self, center: Coordinates, radius: float
    ) -> List[BaseEntity]:
        """Получаем все сущности в заданном радиусе от точки"""
        entities_in_radius = []

        min_x, max_x = center.x - radius, center.x + radius
        min_y, max_y = center.y - radius, center.y + radius

        for dx in range(int(min_x), int(max_x) + 1):
            for dy in range(int(min_y), int(max_y) + 1):
                current_coords = Coordinates(dx, dy)
                if current_coords in self.entities:
                    if center.distance_to(current_coords) <= radius:
                        entities_in_radius.extend(self.entities[current_coords])

        return entities_in_radius

    def teleport_entity_coords(
        self, old_x: int, old_y: int, new_x: int, new_y: int, entity: BaseEntity
    ) -> None:
        old_coords = Coordinates(old_x, old_y)
        new_coords = Coordinates(new_x, new_y)
        self.teleport_entity(old_coords, new_coords, entity)

    def teleport_entity(
        self, old_coords: Coordinates, new_coords: Coordinates, entity: BaseEntity
    ) -> None:
        self.remove_entity(old_coords, entity)
        self.add_entity(new_coords, entity)

    def dump(self) -> Dict[str, Any]:
        """Сериализация карты с вложенными сущностями, используя строки для координат"""
        return {
            "id": self.id,
            "type": self.type,
            "entities": {
                str(coords): [entity.dump() for entity in entity_list]
                for coords, entity_list in self.entities.items()
            },
            "components": {
                type: comp.dump() for type, comp in self._components.items()
            },
        }

    @classmethod
    def restore(cls, data: Dict[str, Any]) -> "MapEntity":
        """Восстановление карты из данных"""
        map_entity = cls(data["id"])

        for coord_str, entities_data in data.get("entities", {}).items():
            coords = Coordinates.from_str(coord_str)
            for entity_data in entities_data:
                entity = Factory.create_entity(entity_data)
                map_entity.add_entity(coords, entity)

        cls._restore_components(map_entity, data)

        return map_entity
