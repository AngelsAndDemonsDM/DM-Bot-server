# Документация по файлу `base_entity.py`


## `Entity.__init__`<br>
Инициализирует объект сущности.<br>
**Args:**<br>
name (str): Имя сущности.<br>
<br>

## `Entity.add_component`<br>
Добавляет компонент к сущности.<br>
**Args:**<br>
component_type (str): Тип компонента.<br>
component_id (str): Идентификатор компонента.<br>
component (Component): Объект компонента.<br>
<br>

## `Entity.get_component`<br>
Возвращает компонент по его типу и идентификатору.<br>
**Args:**<br>
component_type (str): Тип компонента.<br>
component_id (str): Идентификатор компонента.<br>
**Returns:**<br>
Optional[Component]: Объект компонента, если найден, иначе None.<br>
<br>

## `Entity.update`<br>
Обновляет все компоненты сущности.<br>
<br>

## `Entity.to_binary`<br>
Преобразует объект Entity в бинарный формат.<br>
**Returns:**<br>
bytes: Бинарное представление объекта Entity.<br>
<br>

## `Entity.from_binary`<br>
Восстанавливает объект Entity из бинарного формата.<br>
**Args:**<br>
binary_data (bytes): Бинарное представление объекта Entity.<br>
**Returns:**<br>
Entity: Восстановленный объект Entity.<br>
<br>
