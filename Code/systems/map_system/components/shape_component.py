from typing import Any, Dict

from DMBotTools import Shape
from systems.entity_system import BaseComponent

"""
  ...
  components:
    - type: ShapeComponent
      shape: "x" # Считайте как изображение на плоскости. \n - новая строка плоскости. Пробле - пропуск.
      # Пример бублика - "xxx\nx x\nxxx".
      # Если развернуть строку то будет такое на карте:
      # xxx
      # x x
      # xxx
      # Бублик?
"""

class ShapeComponent(BaseComponent):
    __slots__ = ['shape']
    
    def __init__(self, shape: str) -> None:
        super().__init__("ShapeComponent")
        self.shape = Shape(shape)

    def __repr__(self) -> str:
        """Возвращает строковое представление компонента ShapeComponent.

        Returns:
            str: Строковое представление компонента.
        """
        return f"ShapeComponent(shape={self.shape!r})"
    
    @staticmethod
    def get_type_hints() -> Dict[str, Any]:
        """Возвращает словарь с именами переменных и их типами для компонента ShapeComponent.

        Returns:
            Dict[str, Any]: Словарь с именами переменных и их типами.
        """
        return {
            'shape': str
        }
