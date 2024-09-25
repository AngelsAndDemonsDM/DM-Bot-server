from typing import Any, Dict, List, Optional

from systems.ecs import BaseEntity, Factory, register_entity

from .coordinate import Coordinate
from .components import MultiCoordinateComponent


@register_entity
class MapEntity(BaseEntity):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.entities: Dict[Coordinate, List[BaseEntity]] = {}

    def add_entity(
        self, coords: Coordinate | List[Coordinate], entity: BaseEntity
    ) -> None:
        """Добавляем сущность на карту по координатам"""
        if isinstance(coords, list):
            entity.add_component(MultiCoordinateComponent(coords))

        else:
            coords = [coords]

        for cord in coords:
            if cord not in self.entities:
                self.entities[cord] = []

            self.entities[cord].append(entity)

    def get_entities(self, coord: Coordinate, y: int) -> Optional[List[BaseEntity]]:
        return self.entities.get(coord, None)

    def remove_entity(self, coords: Coordinate, entity: BaseEntity) -> None:
        if coords in self.entities:
            if entity in self.entities[coords]:
                comp: MultiCoordinateComponent = entity.get_component(
                    MultiCoordinateComponent().type
                )  # type: ignore
                if comp:
                    for coord in comp.coordinates:
                        self.entities[coord].remove(entity)

                        if not self.entities[coord]:
                            del self.entities[coord]

                else:
                    self.entities[coords].remove(entity)

                    if not self.entities[coords]:
                        del self.entities[coords]

    def get_entities_in_radius(
        self, center: Coordinate, radius: float
    ) -> List[BaseEntity]:
        """Получаем все сущности в заданном радиусе от точки"""
        entities_in_radius = set()

        min_x, max_x = center.x - radius, center.x + radius
        min_y, max_y = center.y - radius, center.y + radius

        for dx in range(int(min_x), int(max_x) + 1):
            for dy in range(int(min_y), int(max_y) + 1):
                current_coords = Coordinate(dx, dy)
                if current_coords in self.entities:
                    if center.distance_to(current_coords) <= radius:
                        entities_in_radius.update(self.entities[current_coords])

        return list(entities_in_radius)

    def teleport_entity(
        self, old_coords: Coordinate, new_coords: Coordinate, entity: BaseEntity
    ) -> None:
        # FIXME:
        self.remove_entity(old_coords, entity)
        self.add_entity(new_coords, entity)

    def dump(self) -> Dict[str, Any]:
        """Сериализация карты с вложенными сущностями, используя строки для координат"""
        return {
            "id": self.id,
            "type": self.type,
            "entitys": {
                str(coords): [entity.dump() for entity in entity_list]
                for coords, entity_list in self.entities.items()
            },
            "components": {
                type: comp.dump() for type, comp in self._components.items()
            },
            "multi_entitys": {},  # FIXME:
        }

    @classmethod
    def restore(cls, data: Dict[str, Any]) -> "MapEntity":
        """Восстановление карты из данных"""
        map_entity = cls(data["id"])

        for coord_str, entityes_data in data.get("entitys", {}).items():
            coords = Coordinate.from_str(coord_str)
            for entity_data in entityes_data:
                entity = Factory.create_entity(entity_data)
                map_entity.add_entity(coords, entity)

        # FIXME:

        cls._restore_components(map_entity, data)

        return map_entity
