# Документация по файлу `SQLDB.py`


## `SQLDB.__init__`<br>
Инициализация класса.<br>
**Args:**<br>
table_name (str): Имя таблицы.<br>
columns (Dict[str, Tuple[type, List[str]]]): Словарь, где ключи - названия столбцов,<br>
а значения - кортежи, содержащие тип данных столбца и список флагов.<br>
db_name (str): Имя базы данных.<br>
db_path (str): Путь к базе данных.<br>
**Examples:**<br>
Создание экземпляра класса SQLDB для работы с таблицей "users" в базе данных "my_db.db" с указанием столбцов "id" (целое число, первичный ключ, автоинкремент), "username" (строка, уникальное значение) и "email" (строка, обязательное поле)<br>
```py
db = SQLDB(
table_name="users",
columns={
"id": (int, ["PRIMARY KEY", "AUTOINCREMENT"]),
"username": (str, ["UNIQUE"]),
"email": (str, ["NOT NULL"])
},
db_name="my_db",
db_path="/path/to/database/"
)
```
<br>

## `SQLDB.__del__`<br>
Деструктор класса.<br>
<br>

## `SQLDB.find`<br>
Выполняет поиск записей в таблице по заданным критериям.<br>
**Args:**<br>
criteria (Dict[str, any]): Критерии поиска.<br>
**Returns:**<br>
List[Dict[str, any]]: Список найденных записей.<br>
**Examples:**<br>
Поиск пользователя по имени пользователя<br>
```py
criteria = {"username": "john_doe"}
found_users = db.find(criteria)
print(found_users)
```
<br>

## `SQLDB.add`<br>
Добавляет запись в таблицу.<br>
**Args:**<br>
record (Dict[str, any]): Запись для добавления.<br>
**Examples:**<br>
Добавление нового пользователя в таблицу<br>
```py
user_record = {"username": "john_doe", "email": "john@example.com"}
db.add(user_record)
```
<br>

## `SQLDB.update`<br>
Обновляет запись в таблице.<br>
**Args:**<br>
record_id (int): Идентификатор записи.<br>
new_values (Dict[str, any]): Новые значения для записи.<br>
**Examples:**<br>
Обновление данных пользователя<br>
```py
updated_values = {"email": "john.doe@example.com"}
db.update(1, updated_values)  
```
Предполагается, что пользователь с ID=1 существует<br>
<br>

## `SQLDB.update_mass`<br>
Массовое обновление записей в таблице.<br>
**Args:**<br>
criteria (Dict[str, any]): Критерии для выбора записей для обновления.<br>
new_values (Dict[str, any]): Новые значения для записей.<br>
**Examples:**<br>
Массовое обновление email у всех пользователей с именем "john_doe"<br>
```py
criteria = {"username": "john_doe"}
new_values = {"email": "john_new@example.com"}
db.update_mass(criteria, new_values)
```
<br>

## `SQLDB.delete`<br>
Удаляет запись из таблицы.<br>
**Args:**<br>
record_id (int): Идентификатор записи.<br>
**Examples:**<br>
Удаление пользователя<br>
```py
db.delete(1)
```
Предполагается, что пользователь с ID=1 существует<br>
<br>

## `SQLDB.delete_mass`<br>
Массовое удаление записей из таблицы.<br>
**Args:**<br>
criteria (Dict[str, any]): Критерии для выбора записей для удаления.<br>
**Examples:**<br>
Массовое удаление пользователей с именем "john_doe"<br>
```py
criteria = {"username": "john_doe"}
db.delete_mass(criteria)
```
<br>

## `SQLDB.get_all_records`<br>
Получает все записи из таблицы.<br>
**Returns:**<br>
List[Dict[str, any]]: Список всех записей из таблицы.<br>
**Examples:**<br>
Получение всех записей из таблицы "users":<br>
```py
all_users = db.get_all_records()
print(all_users)
```
Вывод: [{"id": 1, "username": "john_doe", "email": "john@example.com"}, {"id": 2, "username": "jane_doe", "email": "jane@example.com"}]<br>
<br>
