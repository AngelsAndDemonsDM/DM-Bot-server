import os
from typing import Dict, List, Optional, Type

import yaml
from root_path import ROOT_PATH
from systems.entity_system.base_component import BaseComponent
from systems.entity_system.base_entity import BaseEntity
from systems.map_system import Coordinate


class EntityFactory:
    __slots__ = ['_entity_registry', '_component_registry', '_existing_ids', '_entities']
    
    def __init__(self):
        """Инициализирует фабрику сущностей и регистрирует сущности и компоненты из конфигурационных файлов.
        """
        self._entity_registry: Dict[str, Type[BaseEntity]] = {}
        self._component_registry: Dict[str, Type[BaseComponent]] = {}
        self._existing_ids: Dict[str, List[str]] = {}
        self._entities: List[BaseEntity] = []
        self._register_from_yaml()
        self.load_entities_from_directory(os.path.join(ROOT_PATH, "Prototype"))

    def _register_entity(self, entity_type: str, entity_class: Type[BaseEntity]):
        """Регистрирует класс сущности по его типу.

        Args:
            entity_type (str): Тип сущности.
            entity_class (Type[BaseEntity]): Класс сущности.
        """
        self._entity_registry[entity_type] = entity_class

    def _register_component(self, component_type: str, component_class: Type[BaseComponent]):
        """Регистрирует класс компонента по его типу.

        Args:
            component_type (str): Тип компонента.
            component_class (Type[BaseComponent]): Класс компонента.
        """
        self._component_registry[component_type] = component_class

    def _register_from_yaml(self):
        """Регистрирует сущности и компоненты из YAML файла конфигурации.
        """
        with open(os.path.join(ROOT_PATH, "Prototype", "factory_mappings.yml"), 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        for entity_type, entity_class_name in data.get('entities', {}).items():
            self._register_entity(entity_type, globals()[entity_class_name])

        for component_type, component_class_name in data.get('components', {}).items():
            self._register_component(component_type, globals()[component_class_name])

    def _create_entity(self, entity_data: dict) -> BaseEntity:
        """Создает сущность на основе данных из конфигурации.

        Args:
            entity_data (dict): Данные сущности из конфигурационного файла.

        Raises:
            ValueError: Если тип сущности неизвестен.
            ValueError: Если идентификатор сущности уже существует.

        Returns:
            BaseEntity: Созданная сущность.
        """
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
        """Создает компонент на основе данных из конфигурации.

        Args:
            component_data (dict): Данные компонента из конфигурационного файла.

        Raises:
            ValueError: Если тип компонента неизвестен.
            TypeError: Если данные компонента не соответствуют ожидаемому типу.

        Returns:
            BaseComponent: Созданный компонент.
        """
        component_type = component_data.pop('type')
        component_class = self._component_registry.get(component_type)
        if not component_class:
            raise ValueError(f"Unknown component type: {component_type}")

        type_hints = component_class.get_type_hints()
        for key, expected_type in type_hints.items():
            if key == 'coordinates':
                component_data[key] = [Coordinate.from_dict(coord) for coord in component_data[key]]
            
            if key in component_data and not isinstance(component_data[key], expected_type):
                raise TypeError(f"Expected {key} to be {expected_type} but got {type(component_data[key])}")

        return component_class(**component_data)

    def load_entities_from_yaml(self, file_path: str) -> List[BaseEntity]:
        """Загружает сущности из YAML файла.

        Args:
            file_path (str): Путь к YAML файлу.

        Returns:
            List[BaseEntity]: Список загруженных сущностей.
        """
        with open(file_path, 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        entities = []
        for entity_data in data:
            entity = self._create_entity(entity_data)
            entities.append(entity)

        return entities

    def load_entities_from_directory(self, directory_path: str) -> None:
        """Загружает сущности из всех YAML файлов в указанной директории.

        Args:
            directory_path (str): Путь к директории с YAML файлами.
        """
        self._entities.clear()
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    file_path = os.path.join(root, file)
                    self._entities.extend(self.load_entities_from_yaml(file_path))

    def get_entity_by_id(self, entity_type: str, entity_id: str) -> Optional[BaseEntity]:
        """Возвращает сущность по её типу и идентификатору.

        Args:
            entity_type (str): Тип сущности.
            entity_id (str): Идентификатор сущности.

        Returns:
            Optional[BaseEntity]: Найденная сущность или None, если сущность не найдена.
        """
        for entity in self._entities:
            if entity.id == entity_id and entity.__class__.__name__ == entity_type:
                return entity
        
        return None
