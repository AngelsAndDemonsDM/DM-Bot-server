import copy
from typing import Any, Dict, Optional

from .base_struct import BaseEntity
from .class_roster import ENTITY_REGISTRY


class Factory:
    _id_counter = 0
    _entity_registry_by_uid: Dict[int, BaseEntity] = {}
    _base_entity_registry: Dict[str, BaseEntity] = {}

    @staticmethod
    def _generate_unique_id() -> int:
        Factory._id_counter += 1
        return Factory._id_counter

    @staticmethod
    def create_entity(data: Dict[str, Any]) -> "BaseEntity":
        entity_type = data.get("type")
        entity_class = ENTITY_REGISTRY.get(entity_type)

        if entity_class is None:
            raise ValueError(f"Entity type {entity_type} not found in registry")

        entity = entity_class.restore(data)

        if entity.uid == 0 or entity.uid in Factory._entity_registry_by_uid:
            entity.set_uid(Factory._generate_unique_id())

        Factory._entity_registry_by_uid[entity.uid] = entity

        return entity

    @staticmethod
    def get_entity_by_uid(uid: int) -> Optional["BaseEntity"]:
        return Factory._entity_registry_by_uid.get(uid)

    @staticmethod
    def assign_new_uid_if_needed(entity: "BaseEntity") -> None:
        if entity.uid == 0 or entity.uid in Factory._entity_registry_by_uid:
            entity.set_uid(Factory._generate_unique_id())

        Factory._entity_registry_by_uid[entity.uid] = entity

    @staticmethod
    def register_base_entity(data: Dict[str, Any]) -> "BaseEntity":
        entity_type = data.get("type")
        entity_class = ENTITY_REGISTRY.get(entity_type)

        if entity_class is None:
            raise ValueError(f"Entity type {entity_type} not found in registry")

        entity = entity_class.restore(data)
        Factory._base_entity_registry[entity.id] = entity

        return entity

    @staticmethod
    def get_base_entity_copy(id: str) -> Optional["BaseEntity"]:
        base_entity = Factory._base_entity_registry.get(id, None)

        if base_entity is None:
            return None

        new_entity = copy.deepcopy(base_entity)
        new_entity.set_uid(Factory._generate_unique_id())

        return new_entity
