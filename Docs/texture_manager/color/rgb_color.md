# Документация по файлу `rgb_color.py`


## `RGBColor.__init__`<br>
Инициализирует объект RGBColor с указанными значениями цветов.<br>
**Args:**<br>
color (Tuple[int, int, int, int]) - кортеж с цветами RGBA<br>
**Raises:**<br>
ValueError: Если значения каналов выходят за пределы допустимого диапазона (0-255).<br>
<br>

## `RGBColor.cur_value`<br>
Возвращает значения цветов в формате кортежа (R, G, B, A).<br>
**Returns:**<br>
Tuple[int, int, int, int]: Кортеж, содержащий значения каналов R, G, B и A.<br>
<br>
Устанавливает значения цветов.<br>
**Args:**<br>
values (Tuple[int, int, int, int]): Кортеж, содержащий значения каналов R, G, B и A (0-255).<br>
**Raises:**<br>
ValueError: Если значения каналов выходят за пределы допустимого диапазона (0-255).<br>
<br>

## `RGBColor.get_hex`<br>
Возвращает строковое представление цвета в формате HEX.<br>
**Returns:**<br>
str: Цвет в формате HEX.<br>
<br>
