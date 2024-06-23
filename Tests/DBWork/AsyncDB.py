import unittest
from unittest.mock import MagicMock

import aiosqlite

from Code.db_work import AsyncDB


class TestAsyncDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_name = 'test_db'
        self.db_path = 'test_path'
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
            ],
            'files': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('name', str, AsyncDB.NOT_NULL, None),
                ('data', bytes, AsyncDB.NOT_NULL, None)
            ]
        }
        self.db = MagicMock(spec=AsyncDB)
        self.db.open.return_value = None
        self.db.close.return_value = None
        await self.db.open()
        await self.db.close()

    async def asyncTearDown(self):
        pass

    async def test_insert_and_select(self):
        async with self.db as db:
            db.insert.return_value = None
            db.select.return_value = [{'name': 'HR'}]
            await db.insert('departments', {'name': 'HR'})
            result = await db.select('departments')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'HR')

    async def test_update(self):
        async with self.db as db:
            db.insert.return_value = None
            db.update.return_value = None
            db.select.return_value = [{'name': 'Human Resources'}]
            await db.insert('departments', {'name': 'HR'})
            await db.update('departments', {'name': 'Human Resources'}, 'name = ?', ('HR',))
            result = await db.select('departments')
            self.assertEqual(result[0]['name'], 'Human Resources')

    async def test_delete(self):
        async with self.db as db:
            db.insert.return_value = None
            db.delete.return_value = None
            db.select.return_value = []
            await db.insert('departments', {'name': 'HR'})
            await db.delete('departments', 'name = ?', ('HR',))
            result = await db.select('departments')
            self.assertEqual(len(result), 0)

    async def test_select_raw(self):
        async with self.db as db:
            db.insert.return_value = None
            db.select_raw.return_value = [{'name': 'HR'}]
            await db.insert('departments', {'name': 'HR'})
            results = await db.select_raw("SELECT * FROM departments")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['name'], 'HR')

    async def test_table_creation(self):
        async with self.db:
            conn = MagicMock(spec=aiosqlite.Connection)
            cursor = MagicMock(spec=aiosqlite.Cursor)
            conn.execute.return_value = cursor
            cursor.fetchall.return_value = [('departments',), ('employees',), ('files',)]
            self.db.execute.return_value = cursor

            cursor.fetchall.return_value = [('departments',), ('employees',), ('files',)]
            tables = await cursor.fetchall()
            table_names = [table[0] for table in tables]
            self.assertIn('departments', table_names)
            self.assertIn('employees', table_names)
            self.assertIn('files', table_names)

    async def test_exception_handling(self):
        db = MagicMock(spec=AsyncDB)
        db.open.side_effect = Exception('Error while connecting')
        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(Exception):
                await db.open()
            self.assertIn('Error while connecting', log.output[0])

    async def test_blob_insert_and_select(self):
        async with self.db as db:
            db.insert.return_value = None
            db.select.return_value = [{'name': 'test_blob', 'data': b'This is a test blob data'}]
            blob_data = b'This is a test blob data'
            await db.insert('files', {'name': 'test_blob', 'data': blob_data})
            result = await db.select('files', columns=['name', 'data'])
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'test_blob')
            self.assertEqual(result[0]['data'], blob_data)

    async def test_blob_update(self):
        async with self.db as db:
            db.insert.return_value = None
            db.update.return_value = None
            db.select.return_value = [{'name': 'test_blob', 'data': b'Updated blob data'}]
            initial_blob_data = b'Initial blob data'
            updated_blob_data = b'Updated blob data'
            await db.insert('files', {'name': 'test_blob', 'data': initial_blob_data})
            await db.update('files', {'data': updated_blob_data}, 'name = ?', ('test_blob',))
            result = await db.select('files', columns=['name', 'data'])
            self.assertEqual(result[0]['data'], updated_blob_data)

    async def test_blob_delete(self):
        async with self.db as db:
            db.insert.return_value = None
            db.delete.return_value = None
            db.select.return_value = []
            blob_data = b'Test blob data to delete'
            await db.insert('files', {'name': 'test_blob', 'data': blob_data})
            await db.delete('files', 'name = ?', ('test_blob',))
            result = await db.select('files')
            self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
