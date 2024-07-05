import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite


class AsyncDBError(Exception):
    pass

class UniqueConstraintError(AsyncDBError):
    pass

class ForeignKeyConstraintError(AsyncDBError):
    pass

class CheckConstraintError(AsyncDBError):
    pass

class NotNullConstraintError(AsyncDBError):
    pass

def _handle_integrity_errors(func):
    """_summary_

    Args:
        func (_type_): _description_
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
    PRIMARY_KEY: bytes   = 1 << 0
    AUTOINCREMENT: bytes = 1 << 1
    NOT_NULL: bytes      = 1 << 2
    DEFAULT: bytes       = 1 << 3
    CHECK: bytes         = 1 << 4
    UNIQUE: bytes        = 1 << 5
    FOREIGN_KEY: bytes   = 1 << 6
    
    __slots__ = ['_file_path', '_connect', '_config']
    
    def __init__(self, file_name: str, file_path: str, config: Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]) -> None:
        """_summary_

        Args:
            file_name (str): _description_
            file_path (str): _description_
            config (Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]): _description_

        Raises:
            ValueError: _description_
        
        Example:
            ```py
            |pass
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
        """_summary_

        Args:
            config (Dict[str, List[Tuple[str, type, bytes, Optional[str]]]]): _description_
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
            cursor.execute(create_table_query)

        connect.commit()
        connect.close()
    
    def _get_sql_type(self, sql_type: type) -> str:
        """_summary_

        Args:
            sql_type (type): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
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
        """_summary_

        Args:
            add_info (str): _description_

        Returns:
            Dict[str, str]: _description_
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
        """_summary_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
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
            logging.warning(f"Column '{column_name}': Additional info is empty or None")
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
        """_summary_
        """
        self._connect = await aiosqlite.connect(self._file_path)
        await self._connect.execute("PRAGMA foreign_keys = ON;")
        await self._connect.commit()
    
    async def _close(self) -> None:
        """_summary_
        """
        if self._connect:
            await self._connect.close()
            self._connect = None
    
    async def __aenter__(self) -> 'AsyncDB':
        """_summary_

        Returns:
            AsyncDB: _description_
        
        Example:
            ```py
            |pass
            ```
        """
        await self._open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """_summary_

        Args:
            exc_type (_type_): _description_
            exc (_type_): _description_
            tb (_type_): _description_
        
        Example:
            ```py
            |pass
            ```
        """
        await self._close()
    
    @_handle_integrity_errors
    async def raw(self, query: str, parms: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """_summary_

        Args:
            query (str): _description_
            parms (Optional[Tuple[Any, ...]], optional): _description_. Defaults to None.

        Returns:
            List[Dict[str, Any]]: _description_
        
        Example:
            ```py
            |pass
            ```
        """
        async with self._connect.execute(query, parms or ()) as cursor:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in await cursor.fetchall()]
    
    @_handle_integrity_errors
    async def insert(self, table: str, data: Dict[str, Any]) -> int:
        """_summary_

        Args:
            table (str): _description_
            data (Dict[str, Any]): _description_

        Returns:
            int: _description_
        
        Example:
            ```py
            |pass
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
        """_summary_

        Args:
            table (str): _description_
            data (Dict[str, Any]): _description_
            where (Dict[str, Any]): _description_

        Returns:
            int: _description_
        
        Example:
            ```py
            |pass
            ```
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        async with self._connect.execute(query, tuple(data.values()) + tuple(where.values())) as cursor:
            await self._connect.commit()
            return cursor.rowcount
    
    async def delete(self, table: str, where: Dict[str, Any]) -> int:
        """_summary_

        Args:
            table (str): _description_
            where (Dict[str, Any]): _description_

        Returns:
            int: _description_
        
        Example:
            ```py
            |pass
            ```
        """
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        async with self._connect.execute(query, tuple(where.values())) as cursor:
            await self._connect.commit()
            return cursor.rowcount
    
    async def select(self, table: str, columns: List[str], where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """_summary_

        Args:
            table (str): _description_
            columns (List[str]): _description_
            where (Optional[Dict[str, Any]], optional): _description_. Defaults to None.

        Returns:
            List[Dict[str, Any]]: _description_
        
        Example:
            ```py
            |pass
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
        """_summary_

        Args:
            table (str): _description_
            data (Dict[str, Any]): _description_
            where (Dict[str, Any]): _description_

        Returns:
            int: _description_
        
        Example:
            ```py
            |pass
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
