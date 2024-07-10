from typing import TypedDict


class Coordinate(TypedDict):
    """Класс для представления координат точки на плоскости.

    Args:
        TypedDict: Специальный класс, позволяющий создать словарь с фиксированными ключами и типами значений.

    Attributes:
        x (int): Координата по оси X.
        y (int): Координата по оси Y.
    """
    x: int
    y: int
