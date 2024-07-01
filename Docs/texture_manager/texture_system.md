# Документация по файлу `texture_system.py`


## `TextureSystem.__init__`<br>
Статический класс TextureSystem отвечает за управление текстурами, включая их загрузку, изменение цвета, и объединение слоев в одно изображение или GIF.<br>
<br>

## `TextureSystem.get_textures`<br>
Загружает текстуры из указанного пути.<br>
**Args:**<br>
path (str): Путь к файлу с текстурами.<br>
**Returns:**<br>
List[Dict[str, Any]]: Список текстур.<br>
<br>

## `TextureSystem.get_state_info`<br>
Получает информацию о состоянии текстуры из файла.<br>
**Args:**<br>
path (str): Путь к файлу с текстурами.<br>
state (str): Имя состояния.<br>
**Raises:**<br>
ValueError: Если информация о состоянии не найдена.<br>
**Returns:**<br>
Tuple[int, int, int, bool]: Ширина кадра, высота кадра, количество кадров и флаг маски.<br>
<br>

## `TextureSystem.get_image_recolor`<br>
Возвращает перекрашенное изображение указанного состояния.<br>
**Args:**<br>
path (str): Путь к файлу.<br>
state (str): Имя состояния.<br>
color (Tuple[int, int, int, int], optional): Цвет в формате RGBA. По умолчанию DEFAULT_COLOR.<br>
**Returns:**<br>
Image.Image: Перекрашенное изображение.<br>
<br>

## `TextureSystem.get_image`<br>
Возвращает изображение указанного состояния.<br>
**Args:**<br>
path (str): Путь к файлу.<br>
state (str): Имя состояния.<br>
**Raises:**<br>
FileNotFoundError: Если файл изображения не найден.<br>
**Returns:**<br>
Image.Image: Изображение состояния.<br>
<br>

## `TextureSystem.get_gif_recolor`<br>
Возвращает перекрашенный GIF указанного состояния.<br>
**Args:**<br>
path (str): Путь к файлу.<br>
state (str): Имя состояния.<br>
color (Tuple[int, int, int, int], optional): Цвет в формате RGBA. По умолчанию DEFAULT_COLOR.<br>
fps (int, optional): Частота кадров. По умолчанию DEFAULT_FPS.<br>
**Returns:**<br>
List[Image.Image]: Список кадров перекрашенного GIF.<br>
<br>

## `TextureSystem.get_gif`<br>
Возвращает GIF указанного состояния.<br>
**Args:**<br>
path (str): Путь к файлу.<br>
state (str): Имя состояния.<br>
fps (int, optional): Частота кадров. По умолчанию DEFAULT_FPS.<br>
**Returns:**<br>
List[Image.Image]: Список кадров GIF.<br>
<br>

## `TextureSystem.merge_images`<br>
Накладывает изображение overlay на изображение background с учетом прозрачности.<br>
**Args:**<br>
background (Image.Image): Фоновое изображение.<br>
overlay (Image.Image): Изображение, которое накладывается.<br>
position (Tuple[int, int]): Позиция (x, y), куда будет накладываться overlay. По умолчанию (0, 0).<br>
**Returns:**<br>
Image.Image: Объединенное изображение.<br>
<br>

## `TextureSystem.merge_layers`<br>
Объединяет слои в одно изображение или GIF.<br>
**Args:**<br>
layers (List[Dict[str, Any]]): Список слоев.<br>
fps (int, optional): Частота кадров для GIF. По умолчанию DEFAULT_FPS.<br>
**Returns:**<br>
Union[Image.Image, List[Image.Image]]: Объединенное изображение или список кадров GIF.<br>
<br>
