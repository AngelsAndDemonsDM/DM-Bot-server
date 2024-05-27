# Документация по файлу `dynamic_loader.py`


## `DynamicLoader.__init__`<br>
Инициализирует объект DynamicLoader.<br>
**Args:**<br>
config_dir (str): Путь к директории с конфигурационными файлами.<br>
<br>

## `DynamicLoader.get_entity`<br>
Возвращает объект сущности по ее типу и идентификатору.<br>
**Args:**<br>
entity_type (str): Тип сущности.<br>
entity_id (str): Идентификатор сущности.<br>
**Returns:**<br>
Any: Объект сущности или None, если сущность не найдена.<br>
<br>

## `DynamicLoader.load_entities`<br>
Возвращает список всех загруженных сущностей.<br>
**Returns:**<br>
List[Any]: Список загруженных сущностей.<br>
<br>
