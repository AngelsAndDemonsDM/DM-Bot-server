from abc import ABC
from typing import Dict, Optional, Union

from systems.entity_system.base_component import BaseComponent


class BaseEntity(ABC):
    __slots__ = ['enti_type', 'id', 'uid', 'components']
    
    def __init__(self) -> None:
        """Инициализирует базовую сущность с пустыми идентификатором, типом и словарем компонентов.
        """
        self.id: str = ""
        self.uid: int = None
        self.enti_type: str = ""
        self.components: Dict[str, BaseComponent] = {}
    
    def add_component(self, component: BaseComponent) -> None:
        """Добавляет компонент к сущности.

        Args:
            component (BaseComponent): Компонент, который необходимо добавить.
        """
        self.components[component.comp_type] = component
        component.owner = self
    
    def remove_component(self, component: Union[BaseComponent, str]) -> None:
        """Удаляет компонент из сущности.

        Args:
            component (Union[BaseComponent, str]): Компонент, который необходимо удалить.
        """
        if isinstance(component, BaseComponent):
            component = component.comp_type
        
        if component in self.components:
            self.components[component].owner = None
            del self.components[component]
    
    def get_component(self, component_type: str) -> Optional[BaseComponent]:
        """Возвращает компонент заданного типа, если он существует.

        Args:
            component_type (str): Тип компонента, который необходимо найти.

        Returns:
            Optional[BaseComponent]: Компонент, если найден, иначе None.
        """
        return self.components.get(component_type, None)
