import asyncio
import os
import unittest
import aiosqlite
from Code.db_work import AsyncDB


class TestAsyncDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_name = "test_db"
        self.db_path = "test_path"
        self.db_config = {
            'departments': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('name', str, AsyncDB.NOT_NULL, None)
            ],
            'employees': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('name', str, AsyncDB.NOT_NULL, None),
                ('age', int, AsyncDB.NOT_NULL, None),
                ('email', str, AsyncDB.UNIQUE, None),
                ('department_id', int, AsyncDB.NOT_NULL, 'departments.id')
            ]
        }
        self.db = AsyncDB(self.db_name, self.db_path, self.db_config)

    async def asyncTearDown(self):
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        if os.path.exists(self.db._db_path):
            os.remove(self.db._db_path)

    async def test_insert_and_select(self):
        async with self.db as db:
            await db.insert('departments', {'name': 'HR'})
            result = await db.select('departments')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'HR')

    async def test_update(self):
        async with self.db as db:
            await db.insert('departments', {'name': 'HR'})
            await db.update('departments', {'name': 'Human Resources'}, "name = 'HR'")
            result = await db.select('departments')
            self.assertEqual(result[0]['name'], 'Human Resources')

    async def test_delete(self):
        async with self.db as db:
            await db.insert('departments', {'name': 'HR'})
            await db.delete('departments', "name = 'HR'")
            result = await db.select('departments')
            self.assertEqual(len(result), 0)
    
    async def test_select_raw(self):
        async with self.db as db:
            await db.insert('departments', {'name': 'HR'})
            results = await db.select_raw("SELECT * FROM departments")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['name'], 'HR')

    async def test_table_creation(self):
        async with self.db as db:
            async with aiosqlite.connect(db._db_path) as conn:
                cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = await cursor.fetchall()
                table_names = [table[0] for table in tables]
                self.assertIn('departments', table_names)
                self.assertIn('employees', table_names)

    async def test_close(self):
        async with self.db as db:
            await db.close()
            self.assertIsNone(db._connect)

    async def test_exception_handling(self):
        db = AsyncDB(self.db_name, self.db_path, {})
        with self.assertLogs(level='ERROR') as log:
            await db.open()
            self.assertIn('Error while connecting', log.output[0])

if __name__ == '__main__':
    unittest.main()
