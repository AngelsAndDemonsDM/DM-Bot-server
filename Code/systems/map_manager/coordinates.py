from typing import Dict, Tuple

class Coordinate:
    """Класс для представления координат точки на плоскости.

    Attributes:
        x (int): Координата по оси X.
        y (int): Координата по оси Y.
    """
    __slots__ = ['x', 'y']
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

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
    def distance(coord1: 'Coordinate', coord2: 'Coordinate') -> int:
        """Вычисляет Манхэттенское расстояние между двумя координатами.

        Args:
            coord1 (Coordinate): Первая координата.
            coord2 (Coordinate): Вторая координата.

        Returns:
            int: Манхэттенское расстояние между координатами.
        """
        return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)

    def __repr__(self) -> str:
        return f"Coordinate(x={self.x}, y={self.y})"
