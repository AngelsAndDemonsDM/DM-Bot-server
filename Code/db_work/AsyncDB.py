import asyncio
import logging
import os

import aiosqlite

DBF_PRIMARY_KEY  : bytes = 1 << 0
DBF_UNIQUE       : bytes = 1 << 1
DBF_AUTOINCREMENT: bytes = 1 << 2
DBF_NOT_NULL     : bytes = 1 << 3

class AsyncDB:
    def __init__(self, db_name: str, db_path: str, db_config: dict[str, list[tuple[str, type, bytes, str]]]) -> None:
        """Инициализируйте подключение к базе данных и путь к ней.

        Args:
            db_name (str): Имя базы данных.
            db_path (str): Путь, где будет храниться база данных.
            db_config (dict[str, list[tuple[str, type, bytes, str | None]])]: Конфигурация базы данных.

        Example:
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
        """
        db_path = db_path.replace('/', os.sep)
        db_path = os.path.join(os.getcwd(), "Data.DM-Bot", db_path)

        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        self._db_path: str = os.path.join(db_path, f"{db_name}.db")
        self._connect: aiosqlite.Connection = None
        self._db_config: dict[str, list[tuple[str, type, bytes, str]]] = db_config

    async def __aenter__(self) -> 'AsyncDB':
        self._connect = await aiosqlite.connect(self._db_path)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._connect:
            await self._connect.close()

    def _process_columns(self, columns: list[tuple[str, type, bytes, str]]) -> str:
        table_cfg: list[str] = []
        foreign_keys: list[str] = []

        for column in columns:
            column_def = f"{column[0]} {self._get_column_type(column[1])} {self._get_column_flags(column[2])}".strip()
            table_cfg.append(column_def)
            
            if column[3]:
                ref_table, ref_column = column[3].split('.')
                foreign_keys.append(f"FOREIGN KEY ({column[0]}) REFERENCES {ref_table}({ref_column})")
        
        table_cfg.extend(foreign_keys)
        return ", ".join(table_cfg)

    def _get_column_type(self, datatype: type) -> str:
        match str(datatype):
            case "<class 'int'>" | "<class 'bool'>": return "INTEGER"
            case "<class 'float'>":                  return "REAL"
            case "<class 'str'>":                    return "TEXT"
            case "<class 'bytes'>":                  return "BLOB"
            case _:                                  raise ValueError(f"Unsupported datatype: {datatype}")

    def _get_column_flags(self, flags: bytes) -> str:
        flags_exit: list[str] = []
        
        if flags & DBF_PRIMARY_KEY:
            flags_exit.append("PRIMARY KEY")
        
        if flags & DBF_UNIQUE:
            flags_exit.append("UNIQUE")
        
        if flags & DBF_AUTOINCREMENT:
            flags_exit.append("AUTOINCREMENT")

        if flags & DBF_NOT_NULL:
            flags_exit.append("NOT NULL")

        return " ".join(flags_exit)

    async def open(self) -> None:
        """Открывает базу данных и создайте таблицы в соответствии с конфигурацией.
        """
        async with self:
            try:
                cursor = await self._connect.cursor()

                for table_name, columns in self._db_config.items():
                    table_cfg = self._process_columns(columns)
                    await cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_cfg})")
        
                await self._connect.commit()
                logging.debug(f"Connection with {self._db_path} is open.")
                
            except Exception as err:
                logging.error(f"Error while connecting to {self._db_path}: {err}")
        
    async def close(self) -> None:
        """Закрывает соединение с базой данных.
        """
        if self._connect:
            try:
                await self._connect.close()
            except Exception as err: 
                logging.error(f"Error while closing connection with {self._db_path}: {err}")

    async def insert(self, table: str, data: dict[str, any]) -> None:
        """Вставляет новую запись в указанную таблицу.

        Args:
            table (str): Имя таблицы.
            data (dict[str, any]): Данные для вставки в виде словаря.

        Example:
        ```py
            await db.insert('employees', {'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com', 'department_id': 1})
        ```
        """
        async with self:
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' for _ in data)
            values = tuple(data.values())

            async with self._connect.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values) as cursor:
                await self._connect.commit()

    async def select(self, table: str, columns: list[str] = None, where: str = None) -> list[dict[str, any]]:
        """Выбирает записи из указанной таблицы.

        Args:
            table (str): Имя таблицы.
            columns (список[str], необязательно): Столбцы для извлечения. По умолчанию None (все столбцы).
            where (str, необязательно): Предложение WHERE. По умолчанию - None.

        Returns:
            list[dict[str, any]]: Выбранные записи.

        Example:
        ```py
            results = await db.select('employees', ['name', 'age'], "age > 25")
        ```
        """
        async with self:
            columns_part = ', '.join(columns) if columns else '*'
            where_part = f" WHERE {where}" if where else ''
            async with self._connect.execute(f"SELECT {columns_part} FROM {table}{where_part}") as cursor:
                rows = await cursor.fetchall()
                col_names = [description[0] for description in cursor.description]
                return [dict(zip(col_names, row)) for row in rows]

    async def update(self, table: str, data: dict[str, any], where: str) -> None:
        """Обновляет записей в указанной таблице.

        Args:
            table (str): Имя таблицы.
            data (dict[str, any]): Обновляемые данные в виде словаря.
            where (str): Предложение WHERE, указывающее, какие записи необходимо обновить.

        Example:
        ```py
            await db.update('employees', {'age': 31}, "name = 'John Doe'")
        ```
        """
        async with self:
            set_clause = ', '.join(f"{key} = ?" for key in data.keys())
            values = tuple(data.values())

            async with self._connect.execute(f"UPDATE {table} SET {set_clause} WHERE {where}", values) as cursor:
                await self._connect.commit()

    async def delete(self, table: str, where: str) -> None:
        """Удаляет записей из указанной таблицы.

        Args:
            table (str): Имя таблицы.
            where (str): Предложение WHERE, указывающее, какие записи следует удалить.

        Example:
        ```py
            await db.delete('employees', "name = 'John Doe'")
        ```
        """
        async with self:
            async with self._connect.execute(f"DELETE FROM {table} WHERE {where}") as cursor:
                await self._connect.commit()
