import importlib
import os
from copy import deepcopy
from glob import glob
from typing import Any, Dict, List, Optional

from ruamel.yaml import YAML
from ruamel.yaml.error import MarkedYAMLError


class PrototypeError(Exception):
    __slots__ = ['file_path', 'location', 'message']

    def __init__(self, file_path: str, location: str, message: str) -> None:
        """
        Исключение, возникающее при ошибке в прототипах.

        Args:
            file_path (str): Путь к файлу с ошибкой.
            location (str): Место в файле, где возникла ошибка.
            message (str): Описание ошибки.
        """
        self.file_path = file_path
        self.location = location
        self.message = message
        super().__init__(f"Error in file '{file_path}' at '{location}': {message}")


class PrototypeFactory:
    __slots__ = ['prototype_dir', 'MAPPING_FILE_PATH', 'mapping_data', 'used_ids', 'entities']

    def __init__(self, prototype_dir: str = './Prototype') -> None:
        """
        Инициализация фабрики прототипов.

        Args:
            prototype_dir (str, optional): Директория с файлами прототипов. По умолчанию './Prototype'.

        Raises:
            FileNotFoundError: Если файл factory_mappings.yml не найден в указанной директории.
        """
        self.prototype_dir = prototype_dir
        self.MAPPING_FILE_PATH = os.path.join(prototype_dir, 'factory_mappings.yml')
        
        if not os.path.exists(self.MAPPING_FILE_PATH):
            raise FileNotFoundError(f"The prototype mapping file '{self.MAPPING_FILE_PATH}' does not exist.")
        
        yaml = YAML()
        with open(self.MAPPING_FILE_PATH, 'r', encoding='utf-8') as file:
            self.mapping_data = yaml.load(file)
        
        self.used_ids: Dict[str, set] = {}
        self.entities: Dict[tuple, Any] = {}

    def _load_class(self, class_path: str) -> Any:
        """
        Загрузка класса по строковому пути.

        Args:
            class_path (str): Путь к классу в формате строки.

        Returns:
            Any: Загруженный класс.
        """
        if not class_path.startswith('Code.'):
            class_path = f'Code.{class_path}'
        
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        
        return getattr(module, class_name)
    
    def _create_component(self, component_type: str, **kwargs) -> Any:
        """
        Создание компонента по типу.

        Args:
            component_type (str): Тип компонента.

        Raises:
            PrototypeError: Если тип компонента не найден в mapping_data.

        Returns:
            Any: Созданный компонент.
        """
        component_class_path = self.mapping_data['components'].get(component_type)
        if component_class_path:
            component_class = self._load_class(component_class_path)
            component = component_class(**{**component_class.default_values(), **kwargs})
            return component
        
        else:
            raise PrototypeError(self.MAPPING_FILE_PATH, 'components', f"Component '{component_type}' not found")
    
    def _create_entity(self, entity_data: dict, file_path: str, line_number: int) -> Any:
        """
        Создание сущности по данным из YAML.

        Args:
            entity_data (dict): Данные сущности из YAML.
            file_path (str): Путь к файлу с прототипом.
            line_number (int): Номер строки, где определена сущность.

        Raises:
            PrototypeError: Если не указан тип сущности.
            PrototypeError: Если не указан ID сущности.
            PrototypeError: Если ID уже используется.
            PrototypeError: Если тип сущности не найден в mapping_data.

        Returns:
            Any: Созданная сущность.
        """
        entity_type = entity_data.get('type')
        entity_id = entity_data.get('id')

        if not entity_type:
            raise PrototypeError(file_path, f'line {line_number}', "The 'type' field is required for an entity")
        
        if not entity_id:
            raise PrototypeError(file_path, f'line {line_number}', "The 'id' field is required for an entity")

        if entity_type not in self.used_ids:
            self.used_ids[entity_type] = set()
        
        if entity_id in self.used_ids[entity_type]:
            raise PrototypeError(file_path, f'line {line_number}', f"ID '{entity_id}' for entity type '{entity_type}' already used")
        
        self.used_ids[entity_type].add(entity_id)

        entity_class_path = self.mapping_data['entities'].get(entity_type)
        if entity_class_path:
            entity_class = self._load_class(entity_class_path)
            entity = entity_class(entity_id=entity_id, entity_type=entity_type, **{**entity_class.default_values(), **{k: v for k, v in entity_data.items() if k not in ['type', 'id', 'components']}})
            for component_data in entity_data.get('components', []):
                component = self._create_component(component_data['type'], **{k: v for k, v in component_data.items() if k != 'type'})
                entity.add_component(component_data['type'], component)
            
            self.entities[(entity_type, entity_id)] = entity
            return entity
        
        else:
            raise PrototypeError(file_path, f'line {line_number}', f"Entity '{entity_type}' not found")
    
    def find_entity(self, entity_type: str, entity_id: str) -> Optional[Any]:
        """
        Поиск сущности по типу и ID.

        Args:
            entity_type (str): Тип сущности.
            entity_id (str): ID сущности.

        Returns:
            Optional[Any]: Найденная сущность или None, если сущность не найдена.
        """
        entity_key = (entity_type, entity_id)
        entity = self.entities.get(entity_key)
        if entity:
            return deepcopy(entity)
        
        else:
            return None

    def load_all_entities(self) -> List[Any]:
        """
        Загрузка всех сущностей из YAML файлов.

        Raises:
            PrototypeError: Если возникла ошибка при обработке YAML файлов.

        Returns:
            List[Any]: Список загруженных сущностей.
        """
        entities = []
        yaml = YAML()
        for filename in glob(os.path.join(self.prototype_dir, '**', '*.yml'), recursive=True):
            if 'factory_mappings.yml' in filename:
                continue
            
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    entity_data_list = yaml.load(file)
                    for entity_data in entity_data_list:
                        line_number = entity_data.lc.line + 1
                        try:
                            entity = self._create_entity(entity_data, filename, line_number)
                            entities.append(entity)
                        
                        except PrototypeError as e:
                            raise PrototypeError(e.file_path, e.location, e.message)
                
                except MarkedYAMLError as e:
                    raise PrototypeError(filename, f'line {e.problem_mark.line + 1}', f"YAML Error: {e.problem}")
        
        return entities
