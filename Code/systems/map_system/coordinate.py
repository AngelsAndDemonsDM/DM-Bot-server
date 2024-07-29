import math
from typing import Any, Dict, Tuple, Union


class Coordinate:
    """Класс для представления координат точки на плоскости.

    Attributes:
        x (int): Координата по оси X.
        y (int): Координата по оси Y.
    """
    __slots__ = ['x', 'y']
    
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует объект Coordinate с заданными координатами.

        Args:
            x (int): Координата по оси X.
            y (int): Координата по оси Y.
        """
        self.x = x
        self.y = y

    def __add__(self, value: Union[int, 'Coordinate']) -> 'Coordinate':
        """Складывает заданное значение с координатами.

        Args:
            value (Union[int, 'Coordinate']): Значение для сложения с координатами.

        Returns:
            Coordinate: Новый объект Coordinate с обновленными координатами.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self.x + value.x, self.y + value.y)
        
        return Coordinate(self.x + value, self.y + value)
    
    def __sub__(self, value: Union[int, 'Coordinate']) -> 'Coordinate':
        """Вычитает заданное значение из координат.

        Args:
            value (Union[int, 'Coordinate']): Значение для вычитания из координат.

        Returns:
            Coordinate: Новый объект Coordinate с обновленными координатами.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self.x - value.x, self.y - value.y)
        
        return Coordinate(self.x - value, self.y - value)
    
    def __mul__(self, value: int) -> 'Coordinate':
        """Умножает координаты на заданное значение.

        Args:
            value (int): Значение для умножения координат.

        Returns:
            Coordinate: Новый объект Coordinate с обновленными координатами.
        """
        return Coordinate(self.x * value, self.y * value)

    def __truediv__(self, value: int) -> 'Coordinate':
        """Делит координаты на заданное значение.

        Args:
            value (int): Значение для деления координат.

        Returns:
            Coordinate: Новый объект Coordinate с обновленными координатами.
        """
        if value == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        
        return Coordinate(self.x / value, self.y / value)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        
        return False

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Coordinate.

        Returns:
            str: Строковое представление координат.
        """
        return f"Coordinate(x={self.x}, y={self.y})"

    def to_dict(self) -> Dict[str, int]:
        """Преобразует объект Coordinate в словарь.

        Returns:
            Dict[str, int]: Словарь с координатами.
        """
        return {'x': self.x, 'y': self.y}

    @staticmethod
    def from_dict(data: Dict[str, int]) -> 'Coordinate':
        """Создает объект Coordinate из словаря.

        Args:
            data (Dict[str, int]): Словарь с координатами.

        Returns:
            Coordinate: Новый объект Coordinate.
        """
        return Coordinate(x=data['x'], y=data['y'])

    def to_tuple(self) -> Tuple[int, int]:
        """Преобразует объект Coordinate в кортеж.

        Returns:
            Tuple[int, int]: Кортеж с координатами (x, y).
        """
        return (self.x, self.y)

    @staticmethod
    def from_tuple(data: Tuple[int, int]) -> 'Coordinate':
        """Создает объект Coordinate из кортежа.

        Args:
            data (Tuple[int, int]): Кортеж с координатами (x, y).

        Returns:
            Coordinate: Новый объект Coordinate.
        """
        return Coordinate(x=data[0], y=data[1])

    @staticmethod
    def distance(coord1: 'Coordinate', coord2: 'Coordinate') -> float:
        """Вычисляет расстояние между двумя координатами.

        Args:
            coord1 (Coordinate): Первая координата.
            coord2 (Coordinate): Вторая координата.

        Returns:
            float: Расстояние между двумя координатами.
        """
        return math.sqrt((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2)
