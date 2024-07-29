from typing import Any, Dict

from systems.entity_system import BaseComponent
from systems.map_system.shape import Shape


class ShapeComponent(BaseComponent):
    __slots__ = ['shape']
    
    def __init__(self, shape: str) -> None:
        super().__init__("ShapeComponent")
        self.shape = Shape(shape)

    def __repr__(self) -> str:
        """Возвращает строковое представление компонента MapPhysicsComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"ShapeComponent(shape={self.shape!r})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента MapPhysicsComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'shape': str
        }
