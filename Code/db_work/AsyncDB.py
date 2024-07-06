import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite


class AsyncDBError(Exception):
    """Базовый класс для исключений AsyncDB.
    """
    pass

class UniqueConstraintError(AsyncDBError):
    """Исключение для нарушения ограничения уникальности.
    """
    pass

class ForeignKeyConstraintError(AsyncDBError):
    """Исключение для нарушения ограничения внешнего ключа.
    """
    pass

class CheckConstraintError(AsyncDBError):
    """Исключение для нарушения CHECK ограничения.
    """
    pass

class NotNullConstraintError(AsyncDBError):
    """Исключение для нарушения NOT NULL ограничения.
    """
    pass

def _handle_integrity_errors(func):
    """Декоратор для обработки исключений целостности SQLite.

    Args:
        func (Callable): Функция, которую нужно обернуть.

    Returns:
        Callable: Обернутая функция.
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
    
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise UniqueConstraintError(str(e))
            
            elif "FOREIGN KEY constraint failed" in str(e):
                raise ForeignKeyConstraintError(str(e))
            
            elif "CHECK constraint failed" in str(e):
                raise CheckConstraintError(str(e))
            
            elif "NOT NULL constraint failed" in str(e):
                raise NotNullConstraintError(str(e))
            
            else:
                raise
    
    return wrapper

class AsyncDB:
    """Асинхронный класс для работы с SQLite базой данных."""
    
    PRIMARY_KEY: bytes   = 1 << 0
    AUTOINCREMENT: bytes = 1 << 1
    NOT_NULL: bytes      = 1 << 2
    DEFAULT: bytes       = 1 << 3
    CHECK: bytes         = 1 << 4
    UNIQUE: bytes        = 1 << 5
    FOREIGN_KEY: bytes   = 1 << 6
    
    __slots__ = ['_file_path', '_connect', '_config']
    
    def __init__(self, file_name: str, file_path: str, config: Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]) -> None:
        """Инициализация базы данных.

        Args:
            file_name (str): Имя файла базы данных.
            file_path (str): Путь к директории, где будет храниться файл базы данных.
            config (Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]): Конфигурация базы данных.

        Raises:
            ValueError: Если конфигурация не предоставлена.
        
        Example:
            ```py
            |config = {
            |    'users': [
            |        ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
            |        ('name', str, AsyncDB.NOT_NULL | AsyncDB.UNIQUE, None),
            |        ('age', int, AsyncDB.DEFAULT | AsyncDB.CHECK, 'def.18\\0check.age >= 18'),
            |        ('profile', bytes, AsyncDB.NOT_NULL, None)
            |    ],
            |    'orders': [
            |        ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
            |        ('user_id', int, AsyncDB.NOT_NULL | AsyncDB.FOREIGN_KEY, 'forkey.users.id'),
            |        ('product', str, AsyncDB.NOT_NULL, None)
            |    ]
            |}
            |db = AsyncDB("test_db", "db_path", config)
            ```
        """
        if not config:
            raise ValueError("Database configuration is required")

        file_path = file_path.replace('/', os.sep)
        file_path = os.path.join(os.getcwd(), file_path)

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        self._file_path: str = os.path.join(file_path, f"{file_name}.db")
        self._connect: Optional[aiosqlite.Connection] = None
        self._config = config
        self._init_data_base(config)
    
    def _init_data_base(self, config: Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]) -> None:
        """Инициализация базы данных.

        Args:
            config (Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]): Конфигурация базы данных.
        """
        connect = sqlite3.connect(self._file_path)
        cursor = connect.cursor()

        for table_name, columns in config.items():
            column_definitions = []
            for column in columns:
                column_definition = self._get_column_flags(column, config)
                column_definitions.append(column_definition)
            
            column_definitions_str = ", ".join(column_definitions)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions_str});"
            logging.warning(create_table_query)
            cursor.execute(create_table_query)

        connect.commit()
        connect.close()
    
    def _get_sql_type(self, sql_type: type) -> str:
        """Преобразование типа Python в тип SQL.

        Args:
            sql_type (type): Тип данных Python.

        Raises:
            ValueError: Если тип данных не поддерживается.

        Returns:
            str: Соответствующий тип данных SQL.
        """
        if sql_type is int or sql_type is bool:
            return "INTEGER"
        
        if sql_type is float:
            return "REAL"
        
        if sql_type is bytes:
            return "BLOB"
        
        if sql_type is str:
            return "TEXT"
        
        raise ValueError(f"Unsupported SQL type: {sql_type}")
    
    def _parse_column_add_info(self, add_info: str) -> Dict[str, str]:
        """Парсинг дополнительной информации о колонке.

        Args:
            add_info (str): Дополнительная информация о колонке.

        Returns:
            Dict[str, str]: Словарь с разобранной информацией.
        """
        parsed_info = {}
        if "def." in add_info:
            default_start = add_info.find("def.") + len("def.")
            default_end = add_info.find("\\0", default_start)
            if default_end == -1:
                default_end = len(add_info)
            parsed_info['DEFAULT'] = add_info[default_start:default_end].strip()
        
        if "check." in add_info:
            check_start = add_info.find("check.") + len("check.")
            check_end = add_info.find("\\0", check_start)
            if check_end == -1:
                check_end = len(add_info)
            parsed_info['CHECK'] = add_info[check_start:check_end].strip()
        
        if "forkey." in add_info:
            forkey_start = add_info.find("forkey.") + len("forkey.")
            forkey_end = add_info.find("\\0", forkey_start)
            if forkey_end == -1:
                forkey_end = len(add_info)
            parsed_info['FOREIGN_KEY'] = add_info[forkey_start:forkey_end].strip()

        return parsed_info
    
    def _get_column_flags(self, column: Tuple[str, type, bytes, Optional[str]], config: Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]) -> str:
        """Получение флагов колонки.

        Args:
            column (Tuple[str, type, bytes, Optional[str]]): Информация о колонке.
            config (Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]): Конфигурация базы данных.

        Raises:
            ValueError: Если конфигурация колонки некорректна.

        Returns:
            str: SQL строка с флагами колонки.
        """
        column_name, column_type, column_flags, column_add_info = column
        
        # PRIMARY_KEY не сочетается с типом bytes
        if column_type is bytes and column_flags & AsyncDB.PRIMARY_KEY:
            raise ValueError(f"Column '{column_name}': PRIMARY_KEY cannot be used with byte type")
        
        # PRIMARY_KEY не сочетается с DEFAULT
        if column_flags & AsyncDB.PRIMARY_KEY and column_flags & AsyncDB.DEFAULT:
            raise ValueError(f"Column '{column_name}': PRIMARY_KEY cannot be used with DEFAULT")
        
        # AUTOINCREMENT не сочетается с DEFAULT и CHECK
        if column_flags & AsyncDB.AUTOINCREMENT and (column_flags & AsyncDB.DEFAULT or column_flags & AsyncDB.CHECK):
            raise ValueError(f"Column '{column_name}': AUTOINCREMENT cannot be used with DEFAULT or CHECK")
        
        # AUTOINCREMENT не сочетается ни с чем, кроме int
        if column_flags & AsyncDB.AUTOINCREMENT and column_type is not int:
            raise ValueError(f"Column '{column_name}': AUTOINCREMENT can only be used with int type")
        
        # Проверка для типов TEXT и REAL, которые не поддерживают AUTOINCREMENT
        if column_type in (str, float) and column_flags & AsyncDB.AUTOINCREMENT:
            raise ValueError(f"Column '{column_name}': AUTOINCREMENT cannot be used with TEXT or REAL types")
        
        if column_add_info and column_add_info != "":
            parsed_add_info = self._parse_column_add_info(column_add_info)
        else:
            parsed_add_info = {}
        
        # FOREIGN_KEY должен быть корректным и ссылка должна существовать
        if column_flags & AsyncDB.FOREIGN_KEY:
            if 'FOREIGN_KEY' not in parsed_add_info:
                raise ValueError(f"Column '{column_name}': FOREIGN_KEY specified but no foreign key info provided")
            
            foreign_key_info = parsed_add_info['FOREIGN_KEY']
            ref_table, ref_column = foreign_key_info.split('.')
            if ref_table not in config:
                raise ValueError(f"Referenced table '{ref_table}' for column '{column_name}' does not exist in config")
            
            ref_columns = [col[0] for col in config[ref_table]]
            if ref_column not in ref_columns:
                raise ValueError(f"Referenced column '{ref_column}' in table '{ref_table}' for column '{column_name}' does not exist")
        
        # Генерация строки флагов
        flag_str = ""
        if column_flags & AsyncDB.PRIMARY_KEY:
            flag_str += "PRIMARY KEY "
            
        if column_flags & AsyncDB.AUTOINCREMENT:
            flag_str += "AUTOINCREMENT "
        
        if column_flags & AsyncDB.NOT_NULL:
            flag_str += "NOT NULL "
        
        if column_flags & AsyncDB.DEFAULT and 'DEFAULT' in parsed_add_info:
            flag_str += f"DEFAULT {parsed_add_info['DEFAULT']} "
        
        if column_flags & AsyncDB.CHECK and 'CHECK' in parsed_add_info:
            flag_str += f"CHECK ({parsed_add_info['CHECK']}) "
        
        if column_flags & AsyncDB.UNIQUE:
            flag_str += "UNIQUE "
        
        if column_flags & AsyncDB.FOREIGN_KEY and 'FOREIGN_KEY' in parsed_add_info:
            flag_str += f"REFERENCES {parsed_add_info['FOREIGN_KEY']} "
        
        flag_str = flag_str.strip()
        
        return f'{column_name} {self._get_sql_type(column_type)} {flag_str}'

    async def _open(self) -> None:
        """Открытие асинхронного соединения с базой данных."""
        self._connect = await aiosqlite.connect(self._file_path)
        await self._connect.execute("PRAGMA foreign_keys = ON;")
        await self._connect.commit()
    
    async def _close(self) -> None:
        """Закрытие асинхронного соединения с базой данных."""
        if self._connect:
            await self._connect.close()
            self._connect = None
    
    async def __aenter__(self) -> 'AsyncDB':
        """Вход в контекстное управление.

        Returns:
            AsyncDB: Экземпляр текущего объекта.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    # Используйте db
            ```
        """
        await self._open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Выход из контекстного управления.

        Args:
            exc_type (Type): Тип исключения.
            exc (Exception): Экземпляр исключения.
            tb (Traceback): Трассировка стека.
        """
        await self._close()
    
    @_handle_integrity_errors
    async def raw(self, query: str, parms: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """Выполнение произвольного SQL-запроса.

        Args:
            query (str): SQL-запрос.
            parms (Optional[Tuple[Any, ...]], optional): Параметры для SQL-запроса. Defaults to None.

        Returns:
            List[Dict[str, Any]]: Результат запроса в виде списка словарей.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    result = await db.raw("SELECT * FROM users WHERE age > ?", (20,))
            |    print(result)
            ```
        """
        async with self._connect.execute(query, parms or ()) as cursor:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in await cursor.fetchall()]
    
    @_handle_integrity_errors
    async def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Вставка записи в таблицу.

        Args:
            table (str): Название таблицы.
            data (Dict[str, Any]): Данные для вставки.

        Returns:
            int: ID вставленной записи.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    user_id = await db.insert('users', {
            |        'name': 'Alice',
            |        'age': 30,
            |        'profile': b'Profile data for Alice'
            |    })
            |    print(user_id)
            ```
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        async with self._connect.execute(query, tuple(data.values())) as cursor:
            await self._connect.commit()
            return cursor.lastrowid
    
    @_handle_integrity_errors
    async def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Обновление записи в таблице.

        Args:
            table (str): Название таблицы.
            data (Dict[str, Any]): Данные для обновления.
            where (Dict[str, Any]): Условия для обновления.

        Returns:
            int: Количество обновленных записей.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    rows_affected = await db.update('users', {'age': 31}, {'name': 'Alice'})
            |    print(rows_affected)
            ```
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        async with self._connect.execute(query, tuple(data.values()) + tuple(where.values())) as cursor:
            await self._connect.commit()
            return cursor.rowcount
    
    async def delete(self, table: str, where: Dict[str, Any]) -> int:
        """Удаление записи из таблицы.

        Args:
            table (str): Название таблицы.
            where (Dict[str, Any]): Условия для удаления.

        Returns:
            int: Количество удаленных записей.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    rows_deleted = await db.delete('users', {'name': 'Alice'})
            |    print(rows_deleted)
            ```
        """
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        async with self._connect.execute(query, tuple(where.values())) as cursor:
            await self._connect.commit()
            return cursor.rowcount
    
    async def select(self, table: str, columns: List[str], where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Выборка записей из таблицы.

        Args:
            table (str): Название таблицы.
            columns (List[str]): Список колонок для выборки.
            where (Optional[Dict[str, Any]], optional): Условия для выборки. Defaults to None.

        Returns:
            List[Dict[str, Any]]: Результат выборки в виде списка словарей.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    result = await db.select('users', ['id', 'name', 'age'], {'age': 30})
            |    print(result)
            ```
        """
        columns_str = ', '.join(columns)
        query = f"SELECT {columns_str} FROM {table}"
        parms = ()
        if where:
            where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
            query += f" WHERE {where_clause}"
            parms = tuple(where.values())
        
        async with self._connect.execute(query, parms) as cursor:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in await cursor.fetchall()]

    @_handle_integrity_errors
    async def update_or_insert(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Обновление записи, если она существует; иначе вставка новой записи.

        Args:
            table (str): Название таблицы.
            data (Dict[str, Any]): Данные для обновления или вставки.
            where (Dict[str, Any]): Условия для обновления.

        Returns:
            int: ID обновленной или вставленной записи.
        
        Example:
            ```py
            |async with AsyncDB("test_db", "db_path", config) as db:
            |    user_id = await db.update_or_insert('users', {'age': 31}, {'name': 'Alice'})
            |    print(user_id)
            ```
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        async with self._connect.execute(query, tuple(data.values()) + tuple(where.values())) as cursor:
            await self._connect.commit()
            if cursor.rowcount > 0:
                return cursor.lastrowid

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        async with self._connect.execute(insert_query, tuple(data.values())) as cursor:
            await self._connect.commit()
            return cursor.lastrowid
