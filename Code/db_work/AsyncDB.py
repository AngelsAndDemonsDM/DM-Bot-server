import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite


class AsyncDB:
    PRIMARY_KEY  = 1 << 0
    UNIQUE       = 1 << 1
    AUTOINCREMENT= 1 << 2
    NOT_NULL     = 1 << 3
    
    __slots__ = ['_db_path', '_connect', '_db_config']
    
    def __init__(self, db_name: str, db_path: str, db_config: Dict[str, List[Tuple[str, type, int, Optional[str]]]]) -> None:
        """Инициализирует асинхронное соединение с базой данных SQLite.

        Args:
            db_name (str): Имя базы данных.
            db_path (str): Путь к директории базы данных.
            db_config (Dict[str, List[Tuple[str, type, int, Optional[str]]]]): Конфигурация базы данных в виде словаря,
                где ключи - это имена таблиц, а значения - списки кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).

        Example:
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
        """
        logging.debug("AsyncDB: Initializing database.")
        db_path = db_path.replace('/', os.sep)
        db_path = os.path.join(os.getcwd(), db_path)

        if not os.path.exists(db_path):
            logging.debug(f"AsyncDB: Creating database directory at path: {db_path}")
            os.makedirs(db_path)
        
        self._db_path: str = os.path.join(db_path, f"{db_name}.db")
        self._connect: Optional[aiosqlite.Connection] = None
        self._db_config: Dict[str, List[Tuple[str, type, int, str]]] = db_config
        logging.debug(f"AsyncDB: Database initialized with config: {db_config}")

    async def __aenter__(self) -> 'AsyncDB':
        """Открывает соединение с базой данных при входе в контекст.

        Returns:
            AsyncDB: Текущий экземпляр класса.
        """
        logging.debug("AsyncDB: Entering context, opening connection.")
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Закрывает соединение с базой данных при выходе из контекста."""
        logging.debug("AsyncDB: Exiting context, closing connection.")
        await self.close()

    def _process_columns(self, columns: List[Tuple[str, type, int, Optional[str]]]) -> str:
        """Форматирует описание колонок для SQL запроса.

        Args:
            columns (List[Tuple[str, type, int, Optional[str]]]): Список кортежей, описывающих колонки (имя, тип, флаги, внешние ключи).

        Returns:
            str: SQL строка с описанием колонок и внешних ключей.
        """
        logging.debug(f"AsyncDB: Formatting columns for SQL query: {columns}")
        table_config = self._generate_column_definitions(columns)
        foreign_keys = self._generate_foreign_keys(columns)
        
        if foreign_keys:
            table_config.extend(foreign_keys)
        
        return ", ".join(table_config)

    def _generate_column_definitions(self, columns: List[Tuple[str, type, int, Optional[str]]]) -> List[str]:
        """Генерирует определения колонок для SQL запроса.

        Args:
            columns (List[Tuple[str, type, int, Optional[str]]]): Список кортежей, описывающих колонки.

        Returns:
            List[str]: Список строк с определениями колонок.
        """
        logging.debug(f"AsyncDB: Generating column definitions: {columns}")
        return [
            f"{col[0]} {self._get_column_type(col[1])} {self._get_column_flags(col[2])}".strip()
            for col in columns
        ]

    def _generate_foreign_keys(self, columns: List[Tuple[str, type, int, Optional[str]]]) -> List[str]:
        """Генерирует внешние ключи для SQL запроса.

        Args:
            columns (List[Tuple[str, type, int, Optional[str]]]): Список кортежей, описывающих колонки.

        Returns:
            List[str]: Список строк с определениями внешних ключей.
        """
        logging.debug(f"AsyncDB: Generating foreign keys: {columns}")
        foreign_keys = []
        for col in columns:
            if col[3]:
                try:
                    ref_table, ref_column = col[3].split('.')
                    foreign_keys.append(f"FOREIGN KEY ({col[0]}) REFERENCES {ref_table}({ref_column})")
                except ValueError as err:
                    logging.error(f"Error parsing foreign key for column {col[0]}: {col[3]}")
                    raise ValueError(f"Invalid foreign key format for column {col[0]}: {col[3]}") from err
        return foreign_keys

    def _get_column_type(self, datatype: type) -> str:
        """Определяет SQL тип данных для колонки.

        Args:
            datatype (type): Тип данных Python.

        Raises:
            ValueError: Если тип данных не поддерживается.

        Returns:
            str: SQL тип данных.
        """
        logging.debug(f"AsyncDB: Determining column type for: {datatype}")
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

    def _get_column_flags(self, flags: int) -> str:
        """Определяет SQL флаги для колонки.

        Args:
            flags (int): Битовая маска флагов.

        Returns:
            str: SQL строка с флагами.
        """
        logging.debug(f"AsyncDB: Determining column flags: {flags}")
        flags_exit = []
        if flags & self.PRIMARY_KEY:
            flags_exit.append("PRIMARY KEY AUTOINCREMENT" if flags & self.AUTOINCREMENT else "PRIMARY KEY")
            
        if flags & self.UNIQUE and not (flags & self.PRIMARY_KEY):
            flags_exit.append("UNIQUE")
            
        if flags & self.NOT_NULL:
            flags_exit.append("NOT NULL")
            
        return " ".join(flags_exit)

    async def open(self) -> None:
        """Открывает соединение с базой данных."""
        try:
            logging.debug(f"AsyncDB: Opening connection to database at path: {self._db_path}")
            
            if not self._db_config:
                raise ValueError("Database configuration is required")

            self._connect = await aiosqlite.connect(self._db_path)
            cursor = await self._connect.cursor()

            for table_name, columns in self._db_config.items():
                table_cfg = self._process_columns(columns)
                await cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_cfg})")

            await self._connect.commit()
            logging.debug(f"Connection with {self._db_path} is open.")

        except Exception as err:
            logging.error(f"Error while connecting to {self._db_path}: {err}")
            raise err

    async def close(self) -> None:
        """Закрывает соединение с базой данных."""
        if self._connect:
            try:
                await self._connect.close()
                self._connect = None

            except Exception as err: 
                logging.error(f"Error while closing connection with {self._db_path}: {err}")
                raise err

    async def select_raw(self, query: str, parameters: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """Выполняет произвольный SELECT запрос и возвращает результаты.

        Args:
            query (str): SQL запрос SELECT.
            parameters (Optional[Tuple[Any, ...]], optional): Параметры для запроса.

        Returns:
            List[Dict[str, Any]]: Список строк в виде словарей.

        Example:
        ```py
        |async with async_db as db:
        |    results = await db.select_raw("SELECT * FROM users WHERE name = ?", ("John Doe",))
        |    print(results)
        ```
        """
        logging.debug(f"AsyncDB: Executing SELECT query: {query} with parameters: {parameters}")
        
        async with self._connect.execute(query, parameters) as cursor:
            rows = await cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            return [dict(zip(col_names, row)) for row in rows]

    async def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Выполняет вставку строки в указанную таблицу.

        Args:
            table (str): Имя таблицы.
            data (Dict[str, Any]): Данные для вставки в виде словаря (ключи - имена колонок, значения - данные).

        Returns:
            int: Идентификатор последней вставленной строки.

        Example:
        ```py
        |async with async_db as db:
        |    user_id = await db.insert(
        |        table='users',
        |        data={'name': 'John Doe', 'email': 'john@example.com'}
        |    )
        |    print(f"Inserted user with ID: {user_id}")
        ```
        """
        logging.debug(f"AsyncDB: Executing INSERT into {table}: {data}")
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        values = tuple(data.values())

        async with self._connect.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values) as cursor:
            await self._connect.commit()
            
            return cursor.lastrowid

    async def select(self, table: str, columns: Optional[List[str]] = None, where: Optional[str] = None, where_values: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """Выполняет SELECT запрос и возвращает результаты.

        Args:
            table (str): Имя таблицы.
            columns (Optional[List[str]], optional): Список колонок для выборки. По умолчанию выбираются все колонки.
            where (Optional[str], optional): Условие WHERE для фильтрации. По умолчанию не применяется.
            where_values (Optional[Tuple[Any, ...]], optional): Значения для условия WHERE.

        Returns:
            List[Dict[str, Any]]: Список строк в виде словарей.

        Example:
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
        """
        logging.debug(f"AsyncDB: Executing SELECT in table {table}, columns: {columns}, where: {where}, values: {where_values}")
        columns_part = ', '.join(columns) if columns else '*'
        where_part = f" WHERE {where}" if where else ''

        async with self._connect.execute(f"SELECT {columns_part} FROM {table}{where_part}", where_values) as cursor:
            rows = await cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            return [dict(zip(col_names, row)) for row in rows]

    async def update(self, table: str, data: Dict[str, Any], where: str, where_values: Tuple[Any, ...]) -> None:
        """Выполняет обновление строк в указанной таблице.

        Args:
            table (str): Имя таблицы.
            data (Dict[str, Any]): Данные для обновления в виде словаря (ключи - имена колонок, значения - данные).
            where (str): Условие WHERE для фильтрации строк для обновления.
            where_values (Tuple[Any, ...]): Значения для условия WHERE.

        Example:
        ```py
        |async with async_db as db:
        |    await db.update(
        |        table='users',
        |        data={'name': 'John Smith'},
        |        where='id = ?',
        |        where_values=(1,)
        |    )
        ```
        """
        logging.debug(f"AsyncDB: Executing UPDATE in table {table}, data: {data}, where: {where}, values: {where_values}")
        set_clause = ', '.join(f"{key} = ?" for key in data.keys())
        values = tuple(data.values())

        async with self._connect.execute(f"UPDATE {table} SET {set_clause} WHERE {where}", values + where_values) as cursor:
            await self._connect.commit()


    async def delete(self, table: str, where: str, where_values: Tuple[Any, ...]) -> None:
        """Выполняет удаление строк из указанной таблицы.

        Args:
            table (str): Имя таблицы.
            where (str): Условие WHERE для фильтрации строк для удаления.
            where_values (Tuple[Any, ...]): Значения для условия WHERE.

        Example:
        ```py
        |async with async_db as db:
        |    await db.delete(
        |        table='users',
        |        where='id = ?',
        |        where_values=(1,)
        |    )
        ```
        """
        logging.debug(f"AsyncDB: Executing DELETE from table {table}, where: {where}, values: {where_values}")
        async with self._connect.execute(f"DELETE FROM {table} WHERE {where}", where_values) as cursor:
            await self._connect.commit()
