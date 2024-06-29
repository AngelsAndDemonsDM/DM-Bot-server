# Документация по файлу `texture_system.py`


## `TextureSystem.__init__`<br>
Класс для работы со спрайтами. Используйте уже объявленный из Code.main_impt<br>
**Args:**<br>
path (str): Путь до папки со всеми спрайтами<br>
<br>

## `TextureSystem.is_mask`<br>
Проверка, является ли текстура маской.<br>
**Args:**<br>
path (str): Путь до текстуры.<br>
state (str): Стейт текстуры в пути.<br>
**Returns:**<br>
bool: True, если текстура является маской, иначе False.<br>
<br>

## `TextureSystem.get_texture_and_info`<br>
Метод получения текстуры, координат x и y, является ли маской и количества кадров анимации.<br>
**Args:**<br>
path (str): Путь до текстуры.<br>
state (str): Стейт текстуры в пути.<br>
**Returns:**<br>
Optional[Tuple[Image.Image, int, int, bool, int]]: изображение, x, y, маска ли, количество кадров анимации.<br>
<br>

## `TextureSystem.get_recolor_mask`<br>
Получает или создает перекрашенную маску изображения.<br>
**Args:**<br>
path (str): Путь до папки с изображениями.<br>
state (str): Имя состояния изображения.<br>
color (Tuple[int, int, int, int]): Цвет в формате RGBA.<br>
**Returns:**<br>
Image.Image: Измененное изображение.<br>
<br>

## `TextureSystem.get_gif`<br>
Получает или создает GIF-анимацию из спрайтового листа.<br>
**Args:**<br>
path (str): Путь до папки с изображениями.<br>
state (str): Имя состояния изображения.<br>
fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.<br>
**Returns:**<br>
Image.Image: GIF-анимация.<br>
<br>

## `TextureSystem.get_recolor_gif`<br>
Получает или создает перекрашенную GIF-анимацию из спрайтового листа.<br>
**Args:**<br>
path (str): Путь до папки с изображениями.<br>
state (str): Имя состояния изображения.<br>
color (Tuple[int, int, int, int]): Цвет для перекраски маски.<br>
fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.<br>
**Returns:**<br>
Image.Image: Перекрашенная GIF-анимация.<br>
<br>

## `TextureSystem.merge_layers`<br>
Метод для сложения всех слоев и возврата результата.<br>
**Args:**<br>
layers (List[Dict[str, Any]]): Список словарей, каждый из которых содержит 'path', 'state' и 'color' (необязательно).<br>
fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.<br>
**Returns:**<br>
Union[Image.Image, List[Image.Image]]: Результирующее изображение или список изображений для анимации.<br>
<br>
