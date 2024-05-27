import importlib
import os
from typing import Any, Dict, List, Type

import yaml


class DynamicLoader:
    def __init__(self, config_dir: str):
        """Инициализирует объект DynamicLoader.

        Args:
            config_dir (str): Путь к директории с конфигурационными файлами.
        """
        self.config_dir: str = config_dir
        self.entity_classes: Dict[str, Type] = {}
        self.component_classes: Dict[str, Type] = {}
        self.entities: Dict[str, Any] = {}
        self._load_class_mappings()
        self._load_entities()

    def _load_class_mappings(self) -> None:
        """
        Загружает сопоставления классов сущностей и компонентов из файла class_mappings.yml.
        """
        class_mapping_path = os.path.join(self.config_dir, 'class_mappings.yml')
        
        with open(class_mapping_path, 'r') as file:
            class_mappings = yaml.safe_load(file)
            self.entity_classes = self._import_classes(class_mappings['entities'])
            self.component_classes = self._import_classes(class_mappings['components'])

    def _import_classes(self, class_mapping: Dict[str, str]) -> Dict[str, Type]:
        """Импортирует классы на основе заданного сопоставления.

        Args:
            class_mapping (Dict[str, str]): Словарь с именами классов и их путями.

        Returns:
            Dict[str, Type]: Словарь с именами классов и их объектами типов.
        """
        classes = {}
        
        for class_id, class_path in class_mapping.items():
            module_name, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            classes[class_id] = cls
        
        return classes

    def _load_entities(self) -> None:
        """Загружает все сущности из конфигурационных файлов в директории config_dir.
        """
        for root, _, files in os.walk(self.config_dir):
            for file_name in files:
                if file_name.endswith('.yml') and file_name != 'class_mappings.yml':
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        entity_configs = yaml.safe_load(file)
                        for entity_config in entity_configs:
                            entity = self._create_entity(entity_config)
                            self.entities[entity_config['id']] = entity

    def _create_entity(self, config: Dict[str, Any]) -> Any:
        """Создает объект сущности на основе конфигурации.

        Args:
            config (Dict[str, Any]): Конфигурация сущности.

        Returns:
            Any: Созданный объект сущности.
        """
        entity_type = config['type']
        entity_id = config['id']
        entity_class = self.entity_classes[entity_type]
        entity_params = {k: v for k, v in config.items() if k not in ['type', 'id', 'components']}
        entity = entity_class(**entity_params)
        entity.entity_id = entity_id

        for component_config in config.get('components', []):
            component_type = component_config['type']
            component_id = component_config['id']
            component_class = self.component_classes[component_type]
            component_params = {k: v for k, v in component_config.items() if k not in ['type', 'id']}
            component = component_class(**component_params)
            entity.add_component(component_type, component_id, component)

        return entity

    def get_entity(self, entity_id: str) -> Any:
        """Возвращает объект сущности по ее идентификатору.

        Args:
            entity_id (str): Идентификатор сущности.

        Returns:
            Any: Объект сущности или None, если сущность не найдена.
        """
        return self.entities.get(entity_id)

    def load_entities(self) -> List[Any]:
        """Возвращает список всех загруженных сущностей.

        Returns:
            List[Any]: Список загруженных сущностей.
        """
        return list(self.entities.values())
