# Документация по файлу `tag.py`

## `TagsManager.__init__`<br>
Инициализация объекта Tag.<br>
**Args:**<br>
id (str): Идентификатор тега.<br>
<br>
## `TagsManager.__str__`<br>
Возвращает строковое представление тега.<br>
**Returns:**<br>
str: Строковое представление тега.<br>
<br>
## `TagsManager.id`<br>
Получение ID тега.<br>
**Returns:**<br>
str: ID тега.<br>
<br>
Установка ID тега.<br>
**Args:**<br>
id (str, int, float): Новый идентификатор тега.<br>
<br>
## `TagsManager.find`<br>
Ищет тег в списке тегов.<br>
**Args:**<br>
arr_tags (list): Список тегов для поиска.<br>
tag (str): Тег для поиска.<br>
**Returns:**<br>
bool: True, если тег найден, в противном случае False.<br>
<br>
## `TagsManager.add`<br>
Добавляет тег в список тегов.<br>
**Args:**<br>
arr_tags (list): Список тегов, в который нужно добавить тег.<br>
tag (Tag): Тег для добавления.<br>
**Returns:**<br>
bool: True, если тег успешно добавлен, в противном случае False.<br>
<br>
## `TagsManager.remove`<br>
Удаляет тег из списка тегов.<br>
**Args:**<br>
arr_tags (list): Список тегов, из которого нужно удалить тег.<br>
tag (Tag): Тег для удаления.<br>
**Returns:**<br>
bool: True, если тег успешно удален, в противном случае False.<br>
<br>
## `TagsManager.sort_arr`<br>
Сортирует список тегов по их идентификаторам.<br>
**Args:**<br>
arr_tags (list): Список тегов для сортировки.<br>
<br>
