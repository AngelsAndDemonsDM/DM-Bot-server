# Документация по файлу `texture.py`


## `Texture.__init__`<br>
Инициализирует объект Texture.<br>
**Args:**<br>
path_to_dms (str): Путь к директории с текстурами DMS.<br>
<br>

## `Texture.__getitem__`<br>
Возвращает информацию о состоянии по его имени.<br>
**Args:**<br>
key (str): Имя состояния.<br>
**Returns:**<br>
Optional[Tuple[str, bool, int, Tuple[int, int]]]: Информация о состоянии.<br>
<br>

## `Texture.get_image`<br>
Возвращает изображение для заданного состояния.<br>
**Args:**<br>
state (str): Имя состояния.<br>
**Returns:**<br>
Optional[Image.Image]: Изображение состояния.<br>
<br>

## `Texture.create_gif`<br>
Создает GIF анимацию для заданного состояния.<br>
**Args:**<br>
state (str): Имя состояния.<br>
fps (int, optional): Количество кадров в секунду. Defaults to 60.<br>
**Raises:**<br>
ValueError: Если состояние не найдено.<br>
FileNotFoundError: Если изображение состояния не найдено.<br>
<br>

## `Texture.get_cached_mask`<br>
Возвращает кэшированное изображение маски с заданным цветом.<br>
**Args:**<br>
state (str): Имя состояния.<br>
color (RGBColor): Цвет для перекраски маски.<br>
**Returns:**<br>
Image.Image: Кэшированное изображение маски.<br>
<br>

## `Texture.get_cached_gif`<br>
Возвращает кэшированное GIF изображение для заданного состояния.<br>
**Args:**<br>
state (str): Имя состояния.<br>
fps (int, optional): Количество кадров в секунду. Defaults to 60.<br>
**Returns:**<br>
Image.Image: Кэшированное GIF изображение.<br>
<br>

## `Texture.create_colored_gif`<br>
Создает GIF анимацию с перекрашенной маской для заданного состояния.<br>
**Args:**<br>
state (str): Имя состояния.<br>
color (RGBColor): Цвет для перекраски маски.<br>
fps (int, optional): Количество кадров в секунду. Defaults to 60.<br>
**Raises:**<br>
ValueError: Если состояние не найдено.<br>
FileNotFoundError: Если изображение состояния не найдено.<br>
**Returns:**<br>
Image.Image: GIF анимация с перекрашенной маской.<br>
<br>
