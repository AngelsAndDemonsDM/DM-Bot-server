import asyncio
import logging
import os

import aiosqlite


class AsyncDB:
    PRIMARY_KEY  = 1 << 0
    UNIQUE       = 1 << 1
    AUTOINCREMENT= 1 << 2
    NOT_NULL     = 1 << 3
    
    __slots__ = ['_db_path', '_connect', '_db_config']
    
    def __init__(self, db_name: str, db_path: str, db_config: dict[str, list[tuple[str, type, int, str]]]) -> None:
        """
        Инициализирует асинхронное соединение с базой данных SQLite.

        Args:
            db_name (str): Имя базы данных.
            db_path (str): Путь к директории базы данных.
            db_config (dict[str, list[tuple[str, type, int, str]]]): Конфигурация базы данных в виде словаря,
                где ключи - это имена таблиц, а значения - списки кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).

        Example:
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
        """
        db_path = db_path.replace('/', os.sep)
        db_path = os.path.join(os.getcwd(), db_path)

        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        self._db_path: str = os.path.join(db_path, f"{db_name}.db")
        self._connect: aiosqlite.Connection = None
        self._db_config: dict[str, list[tuple[str, type, int, str]]] = db_config

    async def __aenter__(self) -> 'AsyncDB':
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _process_columns(self, columns: list[tuple[str, type, int, str]]) -> str:
        """
        Форматирует описание колонок для SQL запроса.

        Args:
            columns (list[tuple[str, type, int, str]]): Список кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).

        Returns:
            str: SQL строка с описанием колонок и внешних ключей.

        Example:
        ```py
            >>> columns = [
            ...     ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
            ...     ('name', str, AsyncDB.NOT_NULL, None),
            ...     ('email', str, AsyncDB.UNIQUE, None)
            ... ]
            >>> db._process_columns(columns)
            'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE'
        ```
        """
        table_cfg: list[str] = []
        foreign_keys: list[str] = []

        for column in columns:
            column_def = f"{column[0]} {self._get_column_type(column[1])} {self._get_column_flags(column[2], column[0])}".strip()
            table_cfg.append(column_def)
            
            if column[3]:
                ref_table, ref_column = column[3].split('.')
                foreign_keys.append(f"FOREIGN KEY ({column[0]}) REFERENCES {ref_table}({ref_column})")
        
        table_cfg.extend(foreign_keys)
        return ", ".join(table_cfg)

    def _get_column_type(self, datatype: type) -> str:
        """
        Определяет SQL тип данных для колонки.

        Args:
            datatype (type): Тип данных Python.

        Raises:
            ValueError: Если тип данных не поддерживается.

        Returns:
            str: SQL тип данных.

        Example:
        ```py
            >>> db._get_column_type(int)
            'INTEGER'
            >>> db._get_column_type(str)
            'TEXT'
        ```
        """
        if datatype == int or datatype == bool:
            return "INTEGER"
        
        elif datatype == float:
            return "REAL"
        
        elif datatype == str:
            return "TEXT"
        
        elif datatype == bytes:
            return "BLOB"
        
        else:
            raise ValueError(f"Unsupported datatype: {datatype}")

    def _get_column_flags(self, flags: int, column_name: str) -> str:
        """
        Определяет SQL флаги для колонки.

        Args:
            flags (int): Битовая маска флагов.
            column_name (str): Имя колонки.

        Returns:
            str: SQL строка с флагами.

        Example:
        ```py
            >>> db._get_column_flags(AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, 'id')
            'PRIMARY KEY AUTOINCREMENT'
            >>> db._get_column_flags(AsyncDB.NOT_NULL, 'name')
            'NOT NULL'
        ```
        """
        flags_exit: list[str] = []
        
        if flags & self.PRIMARY_KEY:
            if flags & self.AUTOINCREMENT:
                flags_exit.append("PRIMARY KEY AUTOINCREMENT")
            else:
                flags_exit.append("PRIMARY KEY")
        
        if flags & self.UNIQUE and not (flags & self.PRIMARY_KEY):
            flags_exit.append("UNIQUE")
        
        if flags & self.NOT_NULL:
            flags_exit.append("NOT NULL")

        return " ".join(flags_exit)

    async def open(self) -> None:
        """
        Открывает соединение с базой данных и создает таблицы согласно конфигурации.

        Example:
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
        ```py
        """
        self._connect = await aiosqlite.connect(self._db_path)
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
        """
        Закрывает соединение с базой данных.

        Example:
        ```py
            >>> async with async_db as db:
            ...     await db.close()
        ```py
        """
        if self._connect:
            try:
                await self._connect.close()
            
            except Exception as err: 
                logging.error(f"Error while closing connection with {self._db_path}: {err}")

    async def select_raw(self, query: str) -> list[dict[str, any]]:
        """
        Выполняет произвольный SELECT запрос и возвращает результаты.

        Args:
            query (str): SQL запрос SELECT.

        Returns:
            list[dict[str, any]]: Список строк в виде словарей.

        Example:
        ```py
            >>> async with async_db as db:
            ...     results = await db.select_raw("SELECT * FROM users")
            ...     print(results)
        ```
        """
        async with self._connect.execute(query) as cursor:
            rows = await cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            return [dict(zip(col_names, row)) for row in rows]

    async def insert(self, table: str, data: dict[str, any]) -> int:
        """
        Выполняет вставку строки в указанную таблицу.

        Args:
            table (str): Имя таблицы.
            data (dict[str, any]): Данные для вставки в виде словаря (ключи - имена колонок, значения - данные).

        Returns:
            int: Идентификатор последней вставленной строки.

        Example:
        ```py
            >>> async with async_db as db:
            ...     user_id = await db.insert('users', {'name': 'John Doe', 'email': 'john@example.com'})
            ...     print(user_id)
        ```
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        values = tuple(data.values())

        async with self._connect.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values) as cursor:
            await self._connect.commit()
            return cursor.lastrowid

    async def select(self, table: str, columns: list[str] = None, where: str = None) -> list[dict[str, any]]:
        """
        Выполняет SELECT запрос и возвращает результаты.

        Args:
            table (str): Имя таблицы.
            columns (list[str], optional): Список колонок для выборки. По умолчанию выбираются все колонки.
            where (str, optional): Условие WHERE для фильтрации. По умолчанию не применяется.

        Returns:
            list[dict[str, any]]: Список строк в виде словарей.

        Example:
        ```py
            >>> async with async_db as db:
            ...     users = await db.select('users', ['id', 'name'])
            ...     print(users)
        ```
        """
        columns_part = ', '.join(columns) if columns else '*'
        where_part = f" WHERE {where}" if where else ''
        async with self._connect.execute(f"SELECT {columns_part} FROM {table}{where_part}") as cursor:
            rows = await cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            return [dict(zip(col_names, row)) for row in rows]

    async def update(self, table: str, data: dict[str, any], where: str) -> None:
        """
        Выполняет обновление строк в указанной таблице.

        Args:
            table (str): Имя таблицы.
            data (dict[str, any]): Данные для обновления в виде словаря (ключи - имена колонок, значения - данные).
            where (str): Условие WHERE для фильтрации строк для обновления.

        Example:
        ```py
            >>> async with async_db as db:
            ...     await db.update('users', {'name': 'John Smith'}, "id = 1")
        ```
        """
        set_clause = ', '.join(f"{key} = ?" for key in data.keys())
        values = tuple(data.values())

        async with self._connect.execute(f"UPDATE {table} SET {set_clause} WHERE {where}", values) as cursor:
            await self._connect.commit()

    async def delete(self, table: str, where: str) -> None:
        """
        Выполняет удаление строк из указанной таблицы.

        Args:
            table (str): Имя таблицы.
            where (str): Условие WHERE для фильтрации строк для удаления.

        Example:
        ```py
            >>> async with async_db as db:
            ...     await db.delete('users', "id = 1")
        ```
        """
        async with self._connect.execute(f"DELETE FROM {table} WHERE {where}") as cursor:
            await self._connect.commit()
