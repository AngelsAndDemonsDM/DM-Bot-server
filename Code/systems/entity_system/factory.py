import os
from typing import Any, Dict, List, Type

import yaml
from main_impt import ROOT_PATH
from systems.entity_system.base_component import BaseComponent
from systems.entity_system.base_entity import BaseEntity

# Тут бога нет. Если надо что-то изменить - подумайте дважды.
class EntityFactory:
    __slots__ = ['_entity_registry', '_component_registry', '_existing_ids']
    
    def __init__(self):
        self._entity_registry: Dict[str, Type[BaseEntity]] = {}
        self._component_registry: Dict[str, Type[BaseComponent]] = {}
        self._existing_ids: Dict[str, List[str]] = {}
        self._register_from_yaml()

    def _register_entity(self, entity_type: str, entity_class: Type[BaseEntity]):
        self._entity_registry[entity_type] = entity_class

    def _register_component(self, component_type: str, component_class: Type[BaseComponent]):
        self._component_registry[component_type] = component_class

    def _register_from_yaml(self):
        with open(os.path.join(ROOT_PATH, "Prototype", "factory_mappings.yml"), 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        for entity_type, entity_class_name in data.get('entities', {}).items():
            self._register_entity(entity_type, globals()[entity_class_name])

        for component_type, component_class_name in data.get('components', {}).items():
            self._register_component(component_type, globals()[component_class_name])

    def _create_entity(self, entity_data: dict) -> BaseEntity:
        entity_type = entity_data['type']
        entity_class = self._entity_registry.get(entity_type)
        if not entity_class:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entity_id = entity_data['id']
        
        if entity_type not in self._existing_ids:
            self._existing_ids[entity_type] = []
        
        if entity_id in self._existing_ids[entity_type]:
            raise ValueError(f"Duplicate id {entity_id} for entity type {entity_type}")

        self._existing_ids[entity_type].append(entity_id)

        entity = entity_class()
        entity.id = entity_id

        for component_data in entity_data['components']:
            component = self._create_component(component_data)
            entity.add_component(component)

        return entity

    def _create_component(self, component_data: dict) -> BaseComponent:
        component_type = component_data.pop('type')
        component_class = self._component_registry.get(component_type)
        if not component_class:
            raise ValueError(f"Unknown component type: {component_type}")

        type_hints = component_class.get_type_hints()
        for key, expected_type in type_hints.items():
            if key in component_data and not isinstance(component_data[key], expected_type):
                raise TypeError(f"Expected {key} to be {expected_type} but got {type(component_data[key])}")

        return component_class(**component_data)

    def load_entities_from_yaml(self, file_path: str) -> List[BaseEntity]:
        with open(file_path, 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        entities = []
        for entity_data in data:
            entity = self._create_entity(entity_data)
            entities.append(entity)

        return entities
