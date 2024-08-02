from typing import Any, List

from systems.map_system.coordinate import Coordinate


class Shape:
    """Класс для представления фигуры на плоскости, заданной строковым представлением.
    """
    __slots__ = ['_shape_str']
    
    def __init__(self, shape: str) -> None:
        """Инициализирует объект Shape с заданным строковым представлением фигуры.

        Args:
            shape (str): Строковое представление фигуры.
        """
        self._shape_str: str = shape
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Shape):
            return self._shape_str == other._shape_str
        
        return False
    
    def get_list_coordinates(self) -> List[Coordinate]:
        """Возвращает список координат точек фигуры.

        Returns:
            List[Coordinate]: Список координат, представляющих фигуру.
        """
        shape: List[Coordinate] = []
        for row, line in enumerate(self._shape_str.strip().split('\n')):
            for column, char in enumerate(line):
                if char != " ":
                    shape.append(Coordinate(row, column))
        
        return shape

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Shape.

        Returns:
            str: Строковое представление фигуры.
        """
        return f"Shape(shape={self._shape_str!r})"
