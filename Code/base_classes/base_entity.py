import pickle
from typing import Dict, Optional

from base_classes.base_component import Component


class Entity:
    def __init__(self, entity_id: str):
        """Инициализирует объект сущности.

        Args:
            entity_id (str): Идентификатор сущности.
        """
        self.id: str = entity_id
        self.components: Dict[str, Dict[str, Component]] = {}

    def add_component(self, component_type: str, component_id: str, component: Component) -> None:
        """Добавляет компонент к сущности.

        Args:
            component_type (str): Тип компонента.
            component_id (str): Идентификатор компонента.
            component (Component): Объект компонента.
        """
        component.owner = self
        
        if component_type not in self.components:
            self.components[component_type] = {}
            
        self.components[component_type][component_id] = component

    def get_component(self, component_type: str, component_id: str) -> Optional[Component]:
        """Возвращает компонент по его типу и идентификатору.

        Args:
            component_type (str): Тип компонента.
            component_id (str): Идентификатор компонента.

        Returns:
            Optional[Component]: Объект компонента, если найден, иначе None.
        """
        return self.components.get(component_type, {}).get(component_id)

    def update(self) -> None:
        """Обновляет все компоненты сущности.
        """
        for component_dict in self.components.values():
            for component in component_dict.values():
                component.update()

    def to_binary(self) -> bytes:
        """Преобразует объект Entity в бинарный формат.

        Returns:
            bytes: Бинарное представление объекта Entity.
        """
        return pickle.dumps(self)

    @staticmethod
    def from_binary(binary_data: bytes) -> 'Entity':
        """Восстанавливает объект Entity из бинарного формата.

        Args:
            binary_data (bytes): Бинарное представление объекта Entity.

        Returns:
            Entity: Восстановленный объект Entity.
        """
        return pickle.loads(binary_data)
