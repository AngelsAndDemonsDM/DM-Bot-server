# Документация по файлу `AsyncDB.py`


## `AsyncDB.__init__`<br>
Инициализирует асинхронное соединение с базой данных SQLite.<br>
**Args:**<br>
db_name (str): Имя базы данных.<br>
db_path (str): Путь к директории базы данных.<br>
db_config (Dict[str, List[Tuple[str, type, int, Optional[str]]]]): Конфигурация базы данных в виде словаря,<br>
где ключи - это имена таблиц, а значения - списки кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).<br>
Example:<br>
```py
|db_config = {
|    'users': [
|        ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
|        ('name', str, AsyncDB.NOT_NULL, None),
|        ('email', str, AsyncDB.UNIQUE, None)
|    ]
|}
|async_db = AsyncDB('mydatabase', './db', db_config)
```
<br>

## `AsyncDB.__aenter__`<br>
Открывает соединение с базой данных при входе в контекст.<br>
**Returns:**<br>
AsyncDB: Текущий экземпляр класса.<br>
<br>

## `AsyncDB.__aexit__`<br>
Закрывает соединение с базой данных при выходе из контекста.<br>

## `AsyncDB.initialization`<br>
СИНХРОННЫЙ метод инициализации базы данных.<br>
Позволяет создать базу данных и инициализировать её полностью.<br>
<br>

## `AsyncDB.open`<br>
Открывает соединение с базой данных.<br>

## `AsyncDB.close`<br>
Закрывает соединение с базой данных.<br>

## `AsyncDB.select_raw`<br>
Выполняет произвольный SELECT запрос и возвращает результаты.<br>
**Args:**<br>
query (str): SQL запрос SELECT.<br>
parameters (Optional[Tuple[Any, ...]], optional): Параметры для запроса.<br>
**Returns:**<br>
List[Dict[str, Any]]: Список строк в виде словарей.<br>
Example:<br>
```py
|async with async_db as db:
|    results = await db.select_raw("SELECT * FROM users WHERE name = ?", ("John Doe",))
|    print(results)
```
<br>

## `AsyncDB.insert`<br>
Выполняет вставку строки в указанную таблицу.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (Dict[str, Any]): Данные для вставки в виде словаря (ключи - имена колонок, значения - данные).<br>
**Returns:**<br>
int: Идентификатор последней вставленной строки.<br>
Example:<br>
```py
|async with async_db as db:
|    user_id = await db.insert(
|        table='users',
|        data={'name': 'John Doe', 'email': 'john@example.com'}
|    )
|    print(f"Inserted user with ID: {user_id}")
```
<br>

## `AsyncDB.select`<br>
Выполняет SELECT запрос и возвращает результаты.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
columns (Optional[List[str]], optional): Список колонок для выборки. По умолчанию выбираются все колонки.<br>
where (Optional[str], optional): Условие WHERE для фильтрации. По умолчанию не применяется.<br>
where_values (Optional[Tuple[Any, ...]], optional): Значения для условия WHERE.<br>
**Returns:**<br>
List[Dict[str, Any]]: Список строк в виде словарей.<br>
Example:<br>
```py
|async with async_db as db:
|    users = await db.select(
|        table='users',
|        columns=['id', 'name', 'email'],
|        where='name = ?',
|        where_values=('John Doe',)
|    )
|    print(users)
```
<br>

## `AsyncDB.update`<br>
Выполняет обновление строк в указанной таблице.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (Dict[str, Any]): Данные для обновления в виде словаря (ключи - имена колонок, значения - данные).<br>
where (str): Условие WHERE для фильтрации строк для обновления.<br>
where_values (Tuple[Any, ...]): Значения для условия WHERE.<br>
Example:<br>
```py
|async with async_db as db:
|    await db.update(
|        table='users',
|        data={'name': 'John Smith'},
|        where='id = ?',
|        where_values=(1,)
|    )
```
<br>

## `AsyncDB.delete`<br>
Выполняет удаление строк из указанной таблицы.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
where (str): Условие WHERE для фильтрации строк для удаления.<br>
where_values (Tuple[Any, ...]): Значения для условия WHERE.<br>
Example:<br>
```py
|async with async_db as db:
|    await db.delete(
|        table='users',
|        where='id = ?',
|        where_values=(1,)
|    )
```
<br>
