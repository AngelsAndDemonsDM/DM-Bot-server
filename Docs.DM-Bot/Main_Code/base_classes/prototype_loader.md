# Документация по файлу `prototype_loader.py`


## `PrototypeLoader.__init__`<br>
Инициализатор класса PrototypeLoader.<br>
**Args:**<br>
file_path (str): Путь к каталогу с прототипами.<br>
type (str, optional): Тип прототипа для загрузки. Если не указан, вызывается исключение.<br>
**Raises:**<br>
NotImplementedError: Если тип прототипа не указан.<br>
<br>

## `PrototypeLoader.__getitem__`<br>
Возвращает прототип по его идентификатору.<br>
**Args:**<br>
key (str): Идентификатор прототипа.<br>
**Returns:**<br>
Prototype or None: Возвращает прототип, если найден; в противном случае возвращает None.<br>
<br>

## `PrototypeLoader.prototypes`<br>
Свойство для получения списка всех прототипов.<br>
**Returns:**<br>
list: Список прототипов.<br>
<br>
