# Документация по файлу `hex_color.py`


## `HEXColor.__init__`<br>
Инициализирует объект HEXColor с указанным HEX цветом.<br>
**Args:**<br>
hex_color (str): Цвет в формате HEX. Может начинаться с символа #.<br>
**Raises:**<br>
ValueError: Если переданный HEX цвет имеет неверный формат.<br>
<br>

## `HEXColor.cur_value`<br>
Возвращает строковое представление HEX цвета.<br>
**Returns:**<br>
str: Цвет в формате HEX.<br>
Устанавливает значение цвета класса.<br>
**Args:**<br>
value (str): Цвет в формате HEX.<br>
**Raises:**<br>
ValueError: Если формат HEX цвета неверен.<br>
<br>

## `HEXColor.get_rgba`<br>
Преобразует HEX цвет в формат RGBA.<br>
**Raises:**<br>
ValueError: Если формат HEX цвета неверен (не 6 или 8 символов).<br>
**Returns:**<br>
Tuple[int, int, int, int]: Кортеж, содержащий значения каналов R, G, B и A (0-255).<br>
<br>
