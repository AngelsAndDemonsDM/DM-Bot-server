# Документация по файлу `AsyncDB.py`


## `AsyncDB.__init__`<br>
Инициализирует асинхронное соединение с базой данных SQLite.<br>
**Args:**<br>
db_name (str): Имя базы данных.<br>
db_path (str): Путь к директории базы данных.<br>
db_config (dict[str, list[tuple[str, type, int, str]]]): Конфигурация базы данных в виде словаря,<br>
где ключи - это имена таблиц, а значения - списки кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).<br>
Example:<br>
```py
>>> db_config = {
...     'users': [
...         ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
...         ('name', str, AsyncDB.NOT_NULL, None),
...         ('email', str, AsyncDB.UNIQUE, None)
...     ]
... }
... async_db = AsyncDB('mydatabase', './db', db_config)
```
<br>

## `AsyncDB.open`<br>
Открывает соединение с базой данных и создает таблицы согласно конфигурации.<br>
**Raises:**<br>
ValueError: Если конфигурация базы данных не указана.<br>
err: Если возникает ошибка при подключении к базе данных.<br>
Example:<br>
```py
>>> db_config = {
...     'users': [
...         ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
...         ('name', str, AsyncDB.NOT_NULL, None),
...         ('email', str, AsyncDB.UNIQUE, None)
...     ]
... }
>>> async with async_db as db:
...     await db.open()
```
<br>

## `AsyncDB.close`<br>
Закрывает соединение с базой данных.<br>
**Raises:**<br>
err: Если возникает ошибка при закрытии соединения.<br>
Example:<br>
```py
>>> async with async_db as db:
...     await db.close()
```
<br>

## `AsyncDB.select_raw`<br>
Выполняет произвольный SELECT запрос и возвращает результаты.<br>
**Args:**<br>
query (str): SQL запрос SELECT.<br>
**Returns:**<br>
list[dict[str, any]]: Список строк в виде словарей.<br>
Example:<br>
```py
>>> async with async_db as db:
...     results = await db.select_raw("SELECT * FROM users")
...     print(results)
```
<br>

## `AsyncDB.insert`<br>
Выполняет вставку строки в указанную таблицу.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (dict[str, any]): Данные для вставки в виде словаря (ключи - имена колонок, значения - данные).<br>
**Returns:**<br>
int: Идентификатор последней вставленной строки.<br>
Example:<br>
```py
>>> async with async_db as db:
...     user_id = await db.insert('users', {'name': 'John Doe', 'email': 'john@example.com'})
...     print(user_id)
```
<br>

## `AsyncDB.select`<br>
Выполняет SELECT запрос и возвращает результаты.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
columns (list[str], optional): Список колонок для выборки. По умолчанию выбираются все колонки.<br>
where (str, optional): Условие WHERE для фильтрации. По умолчанию не применяется.<br>
**Returns:**<br>
list[dict[str, any]]: Список строк в виде словарей.<br>
Example:<br>
```py
>>> async with async_db as db:
...     users = await db.select('users', ['id', 'name'])
...     print(users)
```
<br>

## `AsyncDB.update`<br>
Выполняет обновление строк в указанной таблице.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (dict[str, any]): Данные для обновления в виде словаря (ключи - имена колонок, значения - данные).<br>
where (str): Условие WHERE для фильтрации строк для обновления.<br>
Example:<br>
```py
>>> async with async_db as db:
...     await db.update('users', {'name': 'John Smith'}, "id = 1")
```
<br>

## `AsyncDB.delete`<br>
Выполняет удаление строк из указанной таблицы.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
where (str): Условие WHERE для фильтрации строк для удаления.<br>
Example:<br>
```py
>>> async with async_db as db:
...     await db.delete('users', "id = 1")
```
<br>
