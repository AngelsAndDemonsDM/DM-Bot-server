from abc import ABC
from typing import List, Optional

from systems.entity_system.base_component import BaseComponent


class BaseEntity(ABC):
    __slots__ = ['enti_type', 'id', 'components']
    
    def __init__(self) -> None:
        """Инициализирует базовую сущность с пустыми идентификатором, типом и списком компонентов.
        """
        self.id: str = ""
        self.enti_type: str = ""
        self.components: List[BaseComponent] = []
    
    def add_component(self, component: BaseComponent) -> None:
        """Добавляет компонент к сущности.

        Args:
            component (BaseComponent): Компонент, который необходимо добавить.
        """
        self.components.append(component)
        component.owner = self
    
    def remove_component(self, component: BaseComponent) -> None:
        """Удаляет компонент из сущности.

        Args:
            component (BaseComponent): Компонент, который необходимо удалить.
        """
        if component in self.components:
            self.components.remove(component)
            component.owner = None
    
    def get_component(self, component_type: str) -> Optional[BaseComponent]:
        """Возвращает компонент заданного типа, если он существует.

        Args:
            component_type (str): Тип компонента, который необходимо найти.

        Returns:
            Optional[BaseComponent]: Компонент, если найден, иначе None.
        """
        for component in self.components:
            if component.comp_type == component_type:
                return component
        
        return None
