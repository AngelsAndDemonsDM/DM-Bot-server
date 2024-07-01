# Документация по файлу `texture_component.py`


## `TextureComponent.get_layers`<br>
Возвращает все слои в виде списка словарей.<br>
**Returns:**<br>
List[Dict[str, Any]]: Список слоев, каждый из которых является словарем с ключами 'state', 'path' и 'color'.<br>
<br>

## `TextureComponent.add_layer`<br>
Добавляет слой в компонент.<br>
**Args:**<br>
state (str): Состояние слоя.<br>
path (str): Путь к текстуре слоя.<br>
color (List[int], optional): Цвет слоя в формате RGBA. По умолчанию [255, 255, 255, 255].<br>
<br>

## `TextureComponent.remove_layer`<br>
Удаляет слой из компонента по его состоянию.<br>
**Args:**<br>
state (str): Состояние слоя, которое нужно удалить.<br>
<br>

## `TextureComponent.get_layer_path`<br>
Возвращает путь к текстуре слоя по его состоянию.<br>
**Args:**<br>
state (str): Состояние слоя.<br>
**Returns:**<br>
str: Путь к текстуре слоя или None, если слой не найден.<br>
<br>

## `TextureComponent.get_layer_color`<br>
Возвращает цвет слоя по его состоянию.<br>
**Args:**<br>
state (str): Состояние слоя.<br>
**Returns:**<br>
List[int]: Цвет слоя в формате RGBA или None, если слой не найден.<br>
<br>
