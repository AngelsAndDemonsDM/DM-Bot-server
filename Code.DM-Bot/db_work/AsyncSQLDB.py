import asyncio
import logging
import os
from typing import Dict, List, Tuple

import aiosqlite
from db_work import SQLDB


class AsyncSQLDB(SQLDB):
    def __init__(self, table_name: str, columns: Dict[str, Tuple[type, List[str]]], db_name: str, db_path: str) -> None:
        self._connection: aiosqlite.Connection = None
        self._table_name: str = table_name
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._create_connection(db_name, db_path))
        self._loop.run_until_complete(self._create_db(columns))

    async def _create_connection(self, db_name: str, db_path: str) -> None:
        db_path = db_path.replace('/', os.sep)
        db_path = os.path.join(os.getcwd(), 'Data.DM-Bot', db_path)
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        self._connection = await aiosqlite.connect(f"{db_path}/{db_name}.db")

    async def close_connection(self):
        await self._connection.close()

    async def __del__(self):
        try:
            if self._connection is not None:
                await self._connection.close()
        except Exception as err:
            logging.error(f"SQLDB error: __del__: {err}")

    async def find(self, criteria: Dict[str, any]) -> List[Dict[str, any]]:
        async with self._connection.cursor() as cursor:
            conditions = " AND ".join([f"{column} = ?" for column in criteria.keys()])
            values = tuple(criteria.values())
            query = f"SELECT * FROM {self._table_name} WHERE {conditions}"
            await cursor.execute(query, values)
            rows = await cursor.fetchall()

            records = []
            for row in rows:
                record = dict(zip([column[0] for column in cursor.description], row))
                records.append(record)

            return records

    async def add(self, record: Dict[str, any]) -> None:
        async with self._connection.cursor() as cursor:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in range(len(record))])
            values = tuple(record.values())
            query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"
            await cursor.execute(query, values)
            await self._connection.commit()

    async def update(self, record_id: int, new_values: Dict[str, any]) -> None:
        async with self._connection.cursor() as cursor:
            updates = ", ".join([f"{column} = ?" for column in new_values.keys()])
            values = tuple(new_values.values())
            query = f"UPDATE {self._table_name} SET {updates} WHERE id = ?"
            await cursor.execute(query, values + (record_id,))
            await self._connection.commit()

    async def update_mass(self, criteria: Dict[str, any], new_values: Dict[str, any]) -> None:
        records_to_update = await self.find(criteria)

        for record in records_to_update:
            record_id = record["id"]
            await self.update(record_id, new_values)

    async def delete(self, record_id: int) -> None:
        async with self._connection.cursor() as cursor:
            query = f"DELETE FROM {self._table_name} WHERE id = ?"
            await cursor.execute(query, (record_id,))
            await self._connection.commit()

    async def delete_mass(self, criteria: Dict[str, any]) -> None:
        records_to_delete = await self.find(criteria)

        for record in records_to_delete:
            record_id = record["id"]
            await self.delete(record_id)

    async def get_all_records(self) -> List[Dict[str, any]]:
        async with self._connection.cursor() as cursor:
            query = f"SELECT * FROM {self._table_name}"
            await cursor.execute(query)
            rows = await cursor.fetchall()

            records = []
            for row in rows:
                record = dict(zip([column[0] for column in cursor.description], row))
                records.append(record)

            return records
