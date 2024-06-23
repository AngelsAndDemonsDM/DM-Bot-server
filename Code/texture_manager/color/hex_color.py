import re
from typing import Tuple


class HEXColor:
    __slots__ = ["_color"]

    def __init__(self, hex_color: str) -> None:
        """Инициализирует объект HEXColor с указанным HEX цветом.

        Args:
            hex_color (str): Цвет в формате HEX. Может начинаться с символа #.

        Raises:
            ValueError: Если переданный HEX цвет имеет неверный формат.
        """
        hex_color = hex_color.lstrip('#')
        self._validate_hex_color(hex_color)
        self._color = hex_color

    @staticmethod
    def _validate_hex_color(hex_color: str) -> None:
        """Проверяет корректность формата HEX цвета.

        Args:
            hex_color (str): Цвет в формате HEX.

        Raises:
            ValueError: Если формат HEX цвета неверен.
        """
        if not re.fullmatch(r'^[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$', hex_color):
            raise ValueError("Invalid HEX color format. Must be 6 or 8 hexadecimal digits.")

    @property
    def cur_value(self) -> str:
        """Возвращает строковое представление HEX цвета.

        Returns:
            str: Цвет в формате HEX.
        """
        return f"#{self._color}"
    
    @cur_value.setter
    def cur_value(self, value: str) -> None:
        """Устанавливает значение цвета класса.

        Args:
            value (str): Цвет в формате HEX.
            
        Raises:
            ValueError: Если формат HEX цвета неверен.
        """
        value = value.lstrip('#')
        self._validate_hex_color(value)
        self._color = value

    def get_rgba(self) -> Tuple[int, int, int, int]:
        """Преобразует HEX цвет в формат RGBA.

        Raises:
            ValueError: Если формат HEX цвета неверен (не 6 или 8 символов).

        Returns:
            Tuple[int, int, int, int]: Кортеж, содержащий значения каналов R, G, B и A (0-255).
        """
        length = len(self._color)
        if length == 6:
            r, g, b = (int(self._color[i:i+2], 16) for i in (0, 2, 4))
            a = 255
        
        elif length == 8:
            r, g, b, a = (int(self._color[i:i+2], 16) for i in (0, 2, 4, 6))
        
        else:
            raise ValueError("Invalid HEX color format")
        
        return (r, g, b, a)
