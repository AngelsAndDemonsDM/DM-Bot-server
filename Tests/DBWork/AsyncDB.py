import os
import unittest

from Code.db_work import (AsyncDB, CheckConstraintError,
                          ForeignKeyConstraintError, NotNullConstraintError,
                          UniqueConstraintError)


class TestAsyncDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_file = "test_db"
        self.db_path = "test_db_path"
        self.config = {
            'users': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('name', str, AsyncDB.NOT_NULL | AsyncDB.UNIQUE, None),
                ('age', int, AsyncDB.DEFAULT | AsyncDB.CHECK, 'def.18\\0check.age >= 18'),
                ('profile', bytes, AsyncDB.NOT_NULL, None)
            ],
            'orders': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('user_id', int, AsyncDB.NOT_NULL | AsyncDB.FOREIGN_KEY, 'forkey.users.id'),
                ('product', str, AsyncDB.NOT_NULL, None)
            ]
        }
        self.db = AsyncDB(self.db_file, self.db_path, self.config)

    async def asyncTearDown(self):
        if os.path.exists(self.db._file_path):
            os.remove(self.db._file_path)

    async def test_insert_and_select(self):
        async with self.db:
            await self.db.insert('users', {
                'name': 'Alice',
                'age': 30,
                'profile': b'Profile data for Alice'
            })
            result = await self.db.select('users', ['id', 'name', 'age', 'profile'], {'name': 'Alice'})
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[0]['age'], 30)
        self.assertEqual(result[0]['profile'], b'Profile data for Alice')

    async def test_update(self):
        async with self.db:
            await self.db.insert('users', {
                'name': 'Alice',
                'age': 30,
                'profile': b'Profile data for Alice'
            })
            rows_affected = await self.db.update('users', {'age': 31}, {'name': 'Alice'})
            self.assertEqual(rows_affected, 1)
            result = await self.db.select('users', ['id', 'name', 'age', 'profile'], {'name': 'Alice'})
            self.assertEqual(result[0]['age'], 31)

    async def test_delete(self):
        async with self.db:
            await self.db.insert('users', {
                'name': 'Alice',
                'age': 30,
                'profile': b'Profile data for Alice'
            })
            rows_deleted = await self.db.delete('users', {'name': 'Alice'})
            self.assertEqual(rows_deleted, 1)
            result = await self.db.select('users', ['id', 'name', 'age', 'profile'], {'name': 'Alice'})
            self.assertEqual(len(result), 0)

    async def test_update_or_insert(self):
        async with self.db:
            user_id = await self.db.update_or_insert('users', {'age': 31, 'profile': b'Profile data for Bob'}, {'name': 'Bob'})
            result = await self.db.select('users', ['id', 'name', 'age', 'profile'], {'name': 'Bob'})
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['age'], 31)

            user_id = await self.db.update_or_insert('users', {'age': 32, 'profile': b'Updated profile data for Bob'}, {'name': 'Bob'})
            result = await self.db.select('users', ['id', 'name', 'age', 'profile'], {'name': 'Bob'})
            self.assertEqual(result[0]['age'], 32)
            self.assertEqual(result[0]['profile'], b'Updated profile data for Bob')

    async def test_unique_constraint_error(self):
        async with self.db:
            await self.db.insert('users', {
                'name': 'Alice',
                'age': 30,
                'profile': b'Profile data for Alice'
            })
            with self.assertRaises(UniqueConstraintError):
                await self.db.insert('users', {
                    'name': 'Alice',  # Duplicate name
                    'age': 25,
                    'profile': b'Profile data for another Alice'
                })

    async def test_foreign_key_constraint_error(self):
        async with self.db:
            with self.assertRaises(ForeignKeyConstraintError):
                await self.db.insert('orders', {
                    'user_id': 999,  # Non-existent user_id
                    'product': 'Test Product'
                })

    async def test_check_constraint_error(self):
        async with self.db:
            with self.assertRaises(CheckConstraintError):
                await self.db.insert('users', {
                    'name': 'Bob',
                    'age': 17,  # Age less than 18
                    'profile': b'Profile data for Bob'
                })

    async def test_not_null_constraint_error(self):
        async with self.db:
            with self.assertRaises(NotNullConstraintError):
                await self.db.insert('users', {
                    'name': None,  # Name cannot be None
                    'age': 22,
                    'profile': b'Profile data for someone without a name'
                })

if __name__ == '__main__':
    unittest.main()
