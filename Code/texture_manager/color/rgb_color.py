from typing import Tuple


class RGBColor:
    __slots__ = ["_r", "_g", "_b", "_a"]

    def __init__(self, color: Tuple[int, int, int, int]) -> None:
        """
        Инициализирует объект RGBColor с указанными значениями цветов.

        Args:
            color (Tuple[int, int, int, int]) - кортеж с цветами RGBA

        Raises:
            ValueError: Если значения каналов выходят за пределы допустимого диапазона (0-255).
        """
        self._validate_color_value(color)
        self._r, self._g, self._b, self._a = color

    @staticmethod
    def _validate_color_value(values: Tuple[int, int, int, int]) -> None:
        """
        Проверяет, что все значения каналов находятся в пределах допустимого диапазона (0-255).

        Args:
            values (Tuple[int, int, int, int]): Значения каналов.

        Raises:
            ValueError: Если хотя бы одно значение канала выходит за пределы допустимого диапазона (0-255).
        """
        if not all(0 <= value <= 255 for value in values):
            raise ValueError("Invalid RGBA color format. All values must be between 0 and 255")

    @property
    def cur_value(self) -> Tuple[int, int, int, int]:
        """
        Возвращает значения цветов в формате кортежа (R, G, B, A).

        Returns:
            Tuple[int, int, int, int]: Кортеж, содержащий значения каналов R, G, B и A.
        """
        return (self._r, self._g, self._b, self._a)

    @cur_value.setter
    def cur_value(self, values: Tuple[int, int, int, int]) -> None:
        """
        Устанавливает значения цветов.

        Args:
            values (Tuple[int, int, int, int]): Кортеж, содержащий значения каналов R, G, B и A (0-255).

        Raises:
            ValueError: Если значения каналов выходят за пределы допустимого диапазона (0-255).
        """
        self._validate_color_value(values)
        self._r, self._g, self._b, self._a = values

    def get_hex(self) -> str:
        """
        Возвращает строковое представление цвета в формате HEX.

        Returns:
            str: Цвет в формате HEX.
        """
        return f'#{self._r:02X}{self._g:02X}{self._b:02X}{self._a:02X}' if self._a != 255 else f'#{self._r:02X}{self._g:02X}{self._b:02X}'
