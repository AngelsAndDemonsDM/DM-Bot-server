from typing import List

from systems.entity_system.base_component import BaseComponent


class BaseEntity:
    __slots__ = ['enti_type', 'id', 'components']
    
    def __init__(self) -> None:
        self.id: str = ""
        self.enti_type: str = ""
        self.components: List[BaseComponent] = []
    
    def add_component(self, component: BaseComponent) -> None:
        self.components.append(component)
        component.owner = self
    
    def remove_component(self, component: BaseComponent) -> None:
        if component in self.components:
            self.components.remove(component)
            component.owner = None
    
    def get_component(self, component_type: str) -> BaseComponent:
        for component in self.components:
            if component.comp_type == component_type:
                return component
        
        return None
    