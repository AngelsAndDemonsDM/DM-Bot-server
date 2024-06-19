from abc import ABC, abstractmethod


class Entity(ABC):
    __slots__ = ['id', 'type', 'components']

    def __init__(self, entity_id, entity_type):
        self.id = entity_id
        self.type = entity_type
        self.components = {}
    
    def add_component(self, component_name, component):
        self.components[component_name] = component
        component.owner = self
    
    def get_component(self, component_name):
        return self.components.get(component_name)
    
    @abstractmethod
    def __repr__(self):
        pass

    @classmethod
    def default_values(cls):
        return {}
