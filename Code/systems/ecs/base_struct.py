from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .class_roster import COMPONENT_REGISTRY


class BaseEntity(ABC):
    def __init__(self, id: str = "") -> None:
        self._id: str = id
        self._uid: int = 0
        self._components: Dict[str, "BaseComponent"] = {}

    @property
    def id(self) -> str:
        return self._id

    def set_id(self, value: str) -> None:
        self._id = value

    @property
    def uid(self) -> int:
        return self._uid

    def set_uid(self, value: int) -> None:
        self._uid = value

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def add_component(self, comp: "BaseComponent") -> None:
        comp_type = comp.__class__.__name__
        if comp_type in self._components:
            self.remove_component(comp_type)

        comp.set_owner(self)
        self._components[comp_type] = comp

    def remove_component(self, comp_type: str) -> None:
        comp = self._components.pop(comp_type, None)
        if comp is not None:
            comp.set_owner(None)

    def get_component(self, comp_type: str) -> Optional["BaseComponent"]:
        return self._components.get(comp_type, None)

    @abstractmethod
    def dump(self) -> Dict[str, Any]:
        pass  # Подклассы должны переопределить этот метод

        # return {
        #     "id": self._id,
        #     "type": self.type,
        #     "components": {
        #         name: comp.dump() for name, comp in self._components.items()
        #     },
        # }

    @classmethod
    @abstractmethod
    def restore(cls, data: Dict[str, Any]) -> "BaseEntity":
        pass  # Подклассы должны переопределить этот метод

        # entity = cls(id=data["id"])
        # cls._restore_components(entity, data)
        # return entity

    @staticmethod
    def _restore_components(entity: "BaseEntity", data: Dict[str, Any]) -> None:
        components_data = data.get("components", {})
        for comp_type, comp_data in components_data.items():
            component = BaseEntity._create_component(comp_type, comp_data)
            entity.add_component(component)

    @staticmethod
    def _create_component(component_type: str, data: Dict[str, Any]) -> "BaseComponent":
        component_class = COMPONENT_REGISTRY.get(component_type)

        if component_class is None:
            raise ValueError(f"Component type {component_type} not found in registry")

        return component_class.restore(data)


class BaseComponent(ABC):
    def __init__(self) -> None:
        self._owner: Optional["BaseEntity"] = None

    @property
    def owner(self):
        return self._owner

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def set_owner(self, value: Optional["BaseEntity"]) -> None:
        self._owner = value

    @abstractmethod
    def dump(self) -> Dict[str, Any]:
        pass  # Подклассы должны переопределить этот метод

    @classmethod
    @abstractmethod
    def restore(cls, data: Dict[str, Any]) -> "BaseComponent":
        pass  # Подклассы должны переопределить этот метод
