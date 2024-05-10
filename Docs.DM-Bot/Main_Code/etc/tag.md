# Документация по файлу `tag.py`


## `TagsManager.__init__`<br>
Инициализирует новый объект TagsManager.<br>
**Attributes:**<br>
_ids (list): List ID.<br>
<br>

## `TagsManager.find`<br>
Проверяет, существует ли id ID в списке ID.<br>
**Args:**<br>
id (str): Id, который нужно проверить.<br>
**Returns:**<br>
bool: True если ID существует, False в противном случае.<br>
<br>

## `TagsManager.add`<br>
Добавляет новый ID в список ID.<br>
**Args:**<br>
id (str): ID, который нужно добавить.<br>
**Returns:**<br>
bool: True если ID был добавлен, False в противном случае<br>
<br>

## `TagsManager.remove`<br>
Удаляет ID из списка ID.<br>
**Args:**<br>
id (str): ID, который нужно удалить.<br>
**Returns:**<br>
bool: True если ID был удален, False в противном случае.<br>
<br>

## `TagsManager.sort`<br>
Сортирует list ID в алфавитном порядке.<br>
<br>
