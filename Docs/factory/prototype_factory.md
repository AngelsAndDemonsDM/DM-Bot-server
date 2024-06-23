# Документация по файлу `prototype_factory.py`


## `PrototypeFactory.__init__`<br>
Инициализация фабрики прототипов.<br>
**Args:**<br>
prototype_dir (str, optional): Директория с файлами прототипов. По умолчанию './Prototype'.<br>
**Raises:**<br>
FileNotFoundError: Если файл factory_mappings.yml не найден в указанной директории.<br>
<br>

## `PrototypeFactory.find_entity`<br>
Поиск сущности по типу и ID.<br>
**Args:**<br>
entity_type (str): Тип сущности.<br>
entity_id (str): ID сущности.<br>
**Returns:**<br>
Optional[Any]: Найденная сущность или None, если сущность не найдена.<br>
<br>

## `PrototypeFactory.load_all_entities`<br>
Загрузка всех сущностей из YAML файлов.<br>
**Raises:**<br>
PrototypeError: Если возникла ошибка при обработке YAML файлов.<br>
**Returns:**<br>
List[Any]: Список загруженных сущностей.<br>
<br>
