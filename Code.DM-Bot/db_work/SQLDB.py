import logging
import os
import sqlite3
from typing import Dict, List, Tuple


class SQLDB:
    """
    Базовый класс для работы с SQLite базой данных.

    Attributes:
        _connection (sqlite3.Connection): Соединение с базой данных.
        _table_name (str): Имя таблицы.
    """
    def __init__(self, table_name: str, columns: Dict[str, Tuple[type, List[str]]], db_name: str, db_path: str) -> None:
        """
        Инициализация класса.

        Args:
            table_name (str): Имя таблицы.
            columns (Dict[str, Tuple[type, List[str]]]): Словарь, где ключи - названия столбцов,
                а значения - кортежи, содержащие тип данных столбца и список флагов.
            db_name (str): Имя базы данных.
            db_path (str): Путь к базе данных.

        Examples:
            Создание экземпляра класса SQLDB для работы с таблицей "users" в базе данных "my_db.db" с указанием столбцов "id" (целое число, первичный ключ, автоинкремент), "username" (строка, уникальное значение) и "email" (строка, обязательное поле)
            ```py
            db = SQLDB(
                table_name="users",
                columns={
                    "id": (int, ["INTEGER", "PRIMARY KEY", "AUTOINCREMENT"]),
                    "username": (str, ["TEXT", "UNIQUE"]),
                    "email": (str, ["TEXT", "NOT NULL"])
                },
                db_name="my_db",
                db_path="/path/to/database/"
            )
            ```
        """
        self._connection: sqlite3.Connection = None
        self._table_name: str = table_name
        self._create_connection(db_name, db_path)
        self._create_db(columns)

    def _create_connection(self, db_name: str, db_path: str) -> None:
        """
        Создает соединение с базой данных.

        Args:
            db_name (str): Имя базы данных.
            db_path (str): Путь к базе данных.
        """
        db_path = db_name + ".db"
        db_path = db_path.replace('/', os.sep)
        db_path = os.path.join(os.getcwd(), 'Data.DM-Bot', db_path)
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        self._connection = sqlite3.connect(db_path)

    def _create_db(self, columns: Dict[str, Tuple[type, List[str]]]) -> None:
        """
        Создает таблицу в базе данных.

        Args:
            columns (Dict[str, Tuple[type, List[str]]]): Словарь с описанием столбцов таблицы.
        """
        cursor: sqlite3.Cursor = self._connection.cursor()

        columns_str: str = ", ".join([f"{name} {self._get_column_definition(datatype, flags)}" for name, (datatype, flags) in columns.items()])

        query: str = f"CREATE TABLE IF NOT EXISTS {self._table_name} ({columns_str})"

        cursor.execute(query)
        self._connection.commit()
    
    def _get_column_definition(self, datatype: type, flags: List[str]) -> str:
        """
        Возвращает определение столбца.

        Args:
            datatype (type): Тип данных столбца.
            flags (List[str]): Список флагов для столбца.

        Returns:
            str: Определение столбца.
        """
        datatype_str = self._get_sqlite_type(datatype)
        flags_str = self._get_column_flags(flags)
        return f"{datatype_str} {flags_str}"

    def _get_sqlite_type(self, datatype: type) -> str:
        """
        Возвращает тип данных SQLite.

        Args:
            datatype (type): Тип данных.

        Returns:
            str: Тип данных SQLite.
        """
        match str(datatype):
            case "int" | "bool": return "INTEGER"
            case "float":        return "REAL"
            case "str":          return "TEXT"
            case _:              raise ValueError(f"Unsupported datatype: {datatype}")

    def _get_column_flags(self, flags: List[str]) -> str:
        """
        Возвращает строку с флагами столбца.

        Args:
            flags (List[str]): Список флагов для столбца.

        Returns:
            str: Строка с флагами столбца.
        """
        column_flags = []
        for flag in flags:
            match flag:
                case "AUTOINCREMENT": column_flags.append("AUTOINCREMENT")
                case "NOT NULL": column_flags.append("NOT NULL")
                case "PRIMARY KEY": column_flags.append("PRIMARY KEY")
                case "UNIQUE": column_flags.append("UNIQUE")
                case _: raise ValueError(f"Unsupported column flag: {flag}")
                
        return " ".join(column_flags)
    
    def __del__(self):
        """
        Деструктор класса.
        """
        try:
            if self._connection is not None:
                self._connection.close()
        except sqlite3.Error as err:
            logging.error(f"SQLDB error: __del__: {err}")

    def find(self, criteria: Dict[str, any]) -> List[Dict[str, any]]:
        """
        Выполняет поиск записей в таблице по заданным критериям.

        Args:
            criteria (Dict[str, any]): Критерии поиска.

        Returns:
            List[Dict[str, any]]: Список найденных записей.

        Examples:
            Поиск пользователя по имени пользователя
            ```py
            criteria = {"username": "john_doe"}
            found_users = db.find(criteria)
            print(found_users)
            ```
        """
        cursor = self._connection.cursor()

        conditions = " AND ".join([f"{column} = ?" for column in criteria.keys()])
        values = tuple(criteria.values())

        query = f"SELECT * FROM {self._table_name} WHERE {conditions}"
        cursor.execute(query, values)
        rows = cursor.fetchall()

        records = []
        for row in rows:
            record = dict(zip([column[0] for column in cursor.description], row))
            records.append(record)

        return records

    def add(self, record: Dict[str, any]) -> None:
        """
        Добавляет запись в таблицу.

        Args:
            record (Dict[str, any]): Запись для добавления.

        Examples:
            Добавление нового пользователя в таблицу
            ```py
            user_record = {"username": "john_doe", "email": "john@example.com"}
            db.add(user_record)
            ```
        """
        cursor = self._connection.cursor()

        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?" for _ in range(len(record))])
        values = tuple(record.values())

        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        self._connection.commit()

    def update(self, record_id: int, new_values: Dict[str, any]) -> None:
        """
        Обновляет запись в таблице.

        Args:
            record_id (int): Идентификатор записи.
            new_values (Dict[str, any]): Новые значения для записи.

        Examples:
            Обновление данных пользователя
            ```py
            updated_values = {"email": "john.doe@example.com"}
            db.update(1, updated_values)  
            ```
            Предполагается, что пользователь с ID=1 существует
        """
        cursor = self._connection.cursor()

        updates = ", ".join([f"{column} = ?" for column in new_values.keys()])
        values = tuple(new_values.values())
        
        query = f"UPDATE {self._table_name} SET {updates} WHERE id = ?"
        cursor.execute(query, values + (record_id,))
        self._connection.commit()

    def update_mass(self, criteria: Dict[str, any], new_values: Dict[str, any]) -> None:
        """
        Массовое обновление записей в таблице.

        Args:
            criteria (Dict[str, any]): Критерии для выбора записей для обновления.
            new_values (Dict[str, any]): Новые значения для записей.

        Examples:
            Массовое обновление email у всех пользователей с именем "john_doe"
            ```py
            criteria = {"username": "john_doe"}
            new_values = {"email": "john_new@example.com"}
            db.update_mass(criteria, new_values)
            ```
        """
        records_to_update = self.find(criteria)

        for record in records_to_update:
            record_id = record["id"]
            self.update(record_id, new_values)

    def delete(self, record_id: int) -> None:
        """
        Удаляет запись из таблицы.

        Args:
            record_id (int): Идентификатор записи.

        Examples:
            Удаление пользователя
            ```py
            db.delete(1)
            ```
            Предполагается, что пользователь с ID=1 существует
        """
        cursor = self._connection.cursor()

        query = f"DELETE FROM {self._table_name} WHERE id = ?"
        cursor.execute(query, (record_id,))
        self._connection.commit()

    def delete_mass(self, criteria: Dict[str, any]) -> None:
        """
        Массовое удаление записей из таблицы.

        Args:
            criteria (Dict[str, any]): Критерии для выбора записей для удаления.

        Examples:
            Массовое удаление пользователей с именем "john_doe"
            ```py
            criteria = {"username": "john_doe"}
            db.delete_mass(criteria)
            ```
        """
        records_to_delete = self.find(criteria)

        for record in records_to_delete:
            record_id = record["id"]
            self.delete(record_id)
