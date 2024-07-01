# Документация по файлу `texture_validator.py`


## `DMSValidator.validate_dms_dirrect`<br>
Валидирует директорию DMS.<br>
**Args:**<br>
dms_path (str): Путь к директории DMS.<br>
**Returns:**<br>
bool: True, если валидация прошла успешно.<br>
**Raises:**<br>
SpriteValidationError: Если директория не существует, не является директорией или некорректна структура.<br>
<br>

## `DMSValidator.validate_dms`<br>
Валидирует конкретную директорию DMS относительно базового пути.<br>
**Args:**<br>
base_path (str): Базовый путь к директории с текстурами.<br>
dms_path (str): Путь к директории DMS относительно базового пути.<br>
**Returns:**<br>
bool: True, если валидация прошла успешно.<br>
**Raises:**<br>
SpriteValidationError: Если директория не существует, не является директорией или некорректна структура.<br>
<br>

## `DMSValidator.validate_all_dms`<br>
Валидирует все директории DMS в базовой директории.<br>
**Args:**<br>
base_path (str): Базовый путь к директории с текстурами.<br>
**Returns:**<br>
bool: True, если валидация всех директорий прошла успешно.<br>
**Raises:**<br>
SpriteValidationError: Если хотя бы одна директория некорректна.<br>
<br>
