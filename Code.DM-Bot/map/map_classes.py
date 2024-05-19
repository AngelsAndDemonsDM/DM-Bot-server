from typing import Any


class Map:
    def __init__(self, id: str, map_x: int, map_y: int, obj_list: list[Any]) -> None:
        """Конструктор класса карты

        Args:
            id (str): ID карты
            map_x (int): Высота карты
            map_y (int): Длинна карты
            obj_list (list[Any]): Лист объектов находящихся на карте
        """
        self._id: str = id
        self._map_x: int = map_x
        self._map_y: int = map_y
        self._obj_list: int = obj_list

class BaseСoordinateObj:
    def __init__(self, map_x: float, map_y: float) -> None:
        """Базовый класс для работы с координатами любого объекта.

        Args:
            map_x (float): Координата X объекта
            map_y (float): Координата Y объекта
        """
        self._map_x: float = map_x
        self._map_y: float = map_y
    
    @property
    def map_x(self) -> float:
        return self._map_x
    
    def map_x(self, value: float) -> None:
        self._map_x = value
    
    @property
    def map_y(self) -> float:
        return self._map_y
    
    def map_y(self, value: float) -> None:
        self._map_y = value

class MapConnection(BaseСoordinateObj):
    def __init__(self, map_x: float, map_y: float, map_dest_x: float, map_dest_y: float, dest_id: str) -> None:
        """Объект для перемещения между картами. Хранит в себе координаты выхода и целевую карту выхода

        Args:
            map_x (float): Координата X объекта
            map_y (float): Координата Y объекта
            map_dest_x (float): Координаты выхода по X
            map_dest_y (float): Координаты выхода по Y
            dest_id (str): ID целивой карты
        """
        super().__init__(map_x, map_y)
        self._map_dest_x: float = map_dest_x
        self._map_dest_y: float = map_dest_y
        self._dest_id: str = dest_id

    @property
    def map_dest_x(self) -> float:
        return self._map_dest_x
    
    def map_dest_x(self, value: float) -> None:
        self._map_dest_x = value

    @property
    def map_dest_y(self) -> float:
        return self._map_dest_y
    
    def map_dest_y(self, value: float) -> None:
        self._map_dest_y = value

    @property
    def dest_id(self) -> str:
        return self._dest_id
    
    def dest_id(self, value: str) -> None:
        self._dest_id = value
