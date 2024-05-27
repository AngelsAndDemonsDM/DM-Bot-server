# Документация по файлу `AsyncDB.py`


## `AsyncDB.__init__`<br>
Инициализируйте подключение к базе данных и путь к ней.<br>
**Args:**<br>
db_name (str): Имя базы данных.<br>
db_path (str): Путь, где будет храниться база данных.<br>
db_config (dict[str, list[tuple[str, type, bytes, str | None]])]: Конфигурация базы данных.<br>
Example:<br>
```py
AsyncDB = (
db_name = "F"
db_path = "HELP_ME"
db_config = {
'departments': [
('id', int, PRIMARY_KEY | AUTOINCREMENT, None),
('name', str, NOT_NULL, None)
],
'employees': [
('id', int, PRIMARY_KEY | AUTOINCREMENT, None),
('name', str, NOT_NULL, None),
('age', int, NOT_NULL, None),
('email', str, UNIQUE, None),
('department_id', int, NOT_NULL, 'departments.id')
]
}
)
```
<br>

## `AsyncDB.open`<br>
Открывает базу данных и создаёт таблицы в соответствии с конфигурацией.<br>
<br>

## `AsyncDB.close`<br>
Закрывает соединение с базой данных.<br>
<br>

## `AsyncDB.insert`<br>
Вставляет новую запись в указанную таблицу.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (dict[str, any]): Данные для вставки в виде словаря.<br>
Example:<br>
```py
await db.insert('employees', {'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com', 'department_id': 1})
```
<br>

## `AsyncDB.select`<br>
Выбирает записи из указанной таблицы.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
columns (список[str], необязательно): Столбцы для извлечения. По умолчанию None (все столбцы).<br>
where (str, необязательно): Предложение WHERE. По умолчанию - None.<br>
**Returns:**<br>
list[dict[str, any]]: Выбранные записи.<br>
Example:<br>
```py
results = await db.select('employees', ['name', 'age'], "age > 25")
```
<br>

## `AsyncDB.update`<br>
Обновляет записи в указанной таблице.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
data (dict[str, any]): Обновляемые данные в виде словаря.<br>
where (str): Предложение WHERE, указывающее, какие записи необходимо обновить.<br>
Example:<br>
```py
await db.update('employees', {'age': 31}, "name = 'John Doe'")
```
<br>

## `AsyncDB.delete`<br>
Удаляет записи из указанной таблицы.<br>
**Args:**<br>
table (str): Имя таблицы.<br>
where (str): Предложение WHERE, указывающее, какие записи следует удалить.<br>
Example:<br>
```py
await db.delete('employees', "name = 'John Doe'")
```
<br>
