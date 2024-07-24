import importlib
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional, Type

import yaml
from root_path import ROOT_PATH
from systems.decorators import global_class
from systems.entity_system.base_component import BaseComponent
from systems.entity_system.base_entity import BaseEntity


@global_class
class EntityFactory:
    __slots__ = [
        '_entity_registry', '_component_registry', 
        '_entities', '_uid_dict', '_next_uid'
    ]

    def __init__(self):
        self._entity_registry: Dict[str, Type[BaseEntity]] = {}
        self._component_registry: Dict[str, Type[BaseComponent]] = {}
        self._entities: Dict[str, BaseEntity] = {}
        self._uid_dict: Dict[int, BaseEntity] = {}
        self._next_uid: int = 1
        self._register_from_yaml()
        self.load_entities_from_directory(os.path.join(ROOT_PATH, "Prototype"))

    def _register_entity(self, entity_type: str, entity_class: Type[BaseEntity]) -> None:
        """Регистрация класса сущности.

        Args:
            entity_type (str): Тип сущности.
            entity_class (Type[BaseEntity]): Класс сущности.
        """
        self._entity_registry[entity_type] = entity_class

    def _register_component(self, component_type: str, component_class: Type[BaseComponent]) -> None:
        """Регистрация класса компонента.

        Args:
            component_type (str): Тип компонента.
            component_class (Type[BaseComponent]): Класс компонента.
        """
        self._component_registry[component_type] = component_class

    def _import_class(self, full_class_string: str) -> Any:
        """Импорт класса по строковому представлению.

        Args:
            full_class_string (str): Полное строковое представление класса.

        Returns:
            Any: Импортированный класс.
        """
        module_path, class_name = full_class_string.rsplit('.', 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls

    def _register_from_yaml(self) -> None:
        """Регистрация сущностей и компонентов из YAML файла.
        """
        with open(os.path.join(ROOT_PATH, "Prototype", "factory_mappings.yml"), 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        for entity_type, full_class_string in data.get('entities', {}).items():
            entity_class = self._import_class(full_class_string)
            self._register_entity(entity_type, entity_class)

        for component_type, full_class_string in data.get('components', {}).items():
            component_class = self._import_class(full_class_string)
            self._register_component(component_type, component_class)

    def _create_entity(self, entity_data: Dict[str, Any]) -> BaseEntity:
        """Создание сущности по данным из словаря.

        Args:
            entity_data (Dict[str, Any]): Данные сущности.

        Raises:
            ValueError: Если тип сущности неизвестен или найден дубликат ID.

        Returns:
            BaseEntity: Созданная сущность.
        """
        entity_type = entity_data['type']
        entity_class = self._entity_registry.get(entity_type)
        if not entity_class:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entity_id = entity_data['id']
        key = f"{entity_type}_{entity_id}"

        if key in self._entities:
            raise ValueError(f"Duplicate id {entity_id} for entity type {entity_type}")

        entity = entity_class()
        entity.id = entity_id

        for component_data in entity_data['components']:
            component = self._create_component(component_data)
            entity.add_component(component)

        self._entities[key] = entity
        return entity

    def _create_component(self, component_data: Dict[str, Any]) -> BaseComponent:
        """Создание компонента по данным из словаря.

        Args:
            component_data (Dict[str, Any]): Данные компонента.

        Raises:
            ValueError: Если тип компонента неизвестен.
            TypeError: Если тип данных не соответствует ожидаемому.

        Returns:
            BaseComponent: Созданный компонент.
        """
        from systems.map_system.coordinates import Coordinate
        
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
        """Загрузка сущностей из YAML файла.

        Args:
            file_path (str): Путь к YAML файлу.

        Returns:
            List[BaseEntity]: Список загруженных сущностей.
        """
        with open(file_path, 'r', encoding="UTF-8") as file:
            data = yaml.safe_load(file)

        return [self._create_entity(entity_data) for entity_data in data]

    def load_entities_from_directory(self, directory_path: str) -> None:
        """Загрузка сущностей из всех YAML файлов в директории.

        Args:
            directory_path (str): Путь к директории.
        """
        self._entities.clear()
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.yaml', '.yml')) and file != "factory_mappings.yml":
                    file_path = os.path.join(root, file)
                    self._entities.update({f"{entity.type}_{entity.id}": entity for entity in self.load_entities_from_yaml(file_path)})

    def _generate_uid(self) -> int:
        """Генерация уникального идентификатора (UID).

        Returns:
            int: Сгенерированный UID.
        """
        uid = self._next_uid
        self._next_uid += 1
        return uid

    def get_entity_by_id(self, entity_type: str, entity_id: str) -> Optional[BaseEntity]:
        """Получение сущности по типу и ID.

        Args:
            entity_type (str): Тип сущности.
            entity_id (str): ID сущности.

        Returns:
            Optional[BaseEntity]: Сущность, если найдена, иначе None.
        """
        key = f"{entity_type}_{entity_id}"
        if key in self._entities:
            copy_entity = deepcopy(self._entities[key])
            copy_entity.uid = self._generate_uid()
            self._uid_dict[copy_entity.uid] = copy_entity
            return copy_entity
        
        return None

    def get_entity_by_uid(self, uid: int) -> Optional[BaseEntity]:
        """Получение сущности по UID.

        Args:
            uid (int): UID сущности.

        Returns:
            Optional[BaseEntity]: Сущность, если найдена, иначе None.
        """
        return self._uid_dict.get(uid, None)
