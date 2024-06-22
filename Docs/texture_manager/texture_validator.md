# Документация по файлу `texture_validator.py`


## `DMSValidator.__init__`<br>
Инициализирует DMSValidator с указанным путем.<br>
**Args:**<br>
path (str): Относительный путь к папке.<br>
**Raises:**<br>
FileNotFoundError: Если директория не существует.<br>
<br>

## `DMSValidator.validate_dms_dirrect`<br>
_summary_<br>
**Args:**<br>
dms_path (str): _description_<br>
**Returns:**<br>
bool: _description_<br>
<br>

## `DMSValidator.validate_dms`<br>
Проверяет папку DMS.<br>
**Args:**<br>
dms_path (str): Путь к папке DMS относительно корневой папки.<br>
**Returns:**<br>
bool: Результат проверки папки.<br>
<br>

## `DMSValidator.validate_all_dms`<br>
Проверяет все папки с расширением .dms в корневой директории.<br>
**Returns:**<br>
bool: Результат проверки всех папок.<br>
<br>
