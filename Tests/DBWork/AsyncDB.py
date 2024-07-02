import os
import shutil
import unittest

import aiosqlite

from Code.db_work import AsyncDB


class TestAsyncDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_name = 'testdb'
        self.db_path = './test_db_dir'
        self.db_config = {
            'users': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('name', str, AsyncDB.NOT_NULL, None),
                ('email', str, AsyncDB.UNIQUE, None)
            ],
            'posts': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('user_id', int, AsyncDB.NOT_NULL, 'users.id'),
                ('title', str, AsyncDB.NOT_NULL, None),
                ('content', str, 0, None)
            ],
            'data_types': [
                ('id', int, AsyncDB.PRIMARY_KEY | AsyncDB.AUTOINCREMENT, None),
                ('integer_col', int, 0, None),
                ('real_col', float, 0, None),
                ('text_col', str, 0, None),
                ('blob_col', bytes, 0, None)
            ]
        }
        self.async_db = AsyncDB(self.db_name, self.db_path, self.db_config)

    async def asyncTearDown(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

    async def test_insert_and_select(self):
        async with self.async_db as db:
            data = {'name': 'John Doe', 'email': 'john.doe@example.com'}
            user_id = await db.insert('users', data)
            
            self.assertIsNotNone(user_id, "User ID should not be None after insertion")
            
            users = await db.select('users', where='id = ?', where_values=(user_id,))
        
        self.assertEqual(len(users), 1, "Should return one user")
        self.assertEqual(users[0]['name'], 'John Doe', "The name should be 'John Doe'")
        self.assertEqual(users[0]['email'], 'john.doe@example.com', "The email should be 'john.doe@example.com'")

    async def test_update(self):
        async with self.async_db as db:
            data = {'name': 'Jane Doe', 'email': 'jane.doe@example.com'}
            user_id = await db.insert('users', data)
            
            await db.update('users', {'name': 'Jane Smith'}, 'id = ?', (user_id,))
            
            users = await db.select('users', where='id = ?', where_values=(user_id,))
        
        self.assertEqual(len(users), 1, "Should return one user")
        self.assertEqual(users[0]['name'], 'Jane Smith', "The name should be 'Jane Smith'")

    async def test_delete(self):
        async with self.async_db as db:
            data = {'name': 'Jake Doe', 'email': 'jake.doe@example.com'}
            user_id = await db.insert('users', data)
            
            await db.delete('users', 'id = ?', (user_id,))
            
            users = await db.select('users', where='id = ?', where_values=(user_id,))
        
        self.assertEqual(len(users), 0, "No user should be returned after deletion")

    async def test_foreign_key_constraint(self):
        async with self.async_db as db:
            user_data = {'name': 'Alice', 'email': 'alice@example.com'}
            user_id = await db.insert('users', user_data)

            post_data = {'user_id': user_id, 'title': 'First Post', 'content': 'This is a post.'}
            post_id = await db.insert('posts', post_data)

            posts = await db.select('posts', where='id = ?', where_values=(post_id,))

        self.assertEqual(len(posts), 1, "Should return one post")
        self.assertEqual(posts[0]['title'], 'First Post', "The title should be 'First Post'")
        self.assertEqual(posts[0]['content'], 'This is a post.', "The content should be 'This is a post.'")

    async def test_select_raw(self):
        async with self.async_db as db:
            data = {'name': 'Bob', 'email': 'bob@example.com'}
            user_id = await db.insert('users', data)

            query = "SELECT * FROM users WHERE id = ?"
            users = await db.select_raw(query, (user_id,))

        self.assertEqual(len(users), 1, "Should return one user")
        self.assertEqual(users[0]['name'], 'Bob', "The name should be 'Bob'")
        self.assertEqual(users[0]['email'], 'bob@example.com', "The email should be 'bob@example.com'")

    async def test_insert_with_duplicate_email(self):
        data1 = {'name': 'Charlie', 'email': 'charlie@example.com'}
        data2 = {'name': 'Charlie2', 'email': 'charlie@example.com'}

        async with self.async_db as db:
            await db.insert('users', data1)

            with self.assertRaises(aiosqlite.IntegrityError):
                await db.insert('users', data2)

    async def test_update_with_nonexistent_id(self):
        async with self.async_db as db:
            await db.update('users', {'name': 'Nonexistent'}, 'id = ?', (999,))

            users = await db.select('users', where='id = ?', where_values=(999,))
        
        self.assertEqual(len(users), 0, "No user should be returned for nonexistent id")

    async def test_delete_with_nonexistent_id(self):
        async with self.async_db as db:
            await db.delete('users', 'id = ?', (999,))

            users = await db.select('users', where='id = ?', where_values=(999,))
        
        self.assertEqual(len(users), 0, "No user should be returned for nonexistent id")

    async def test_foreign_key_violation(self):
        post_data = {'user_id': 999, 'title': 'Invalid Post', 'content': 'Invalid content.'}

        async with self.async_db as db:
            with self.assertRaises(aiosqlite.IntegrityError):
                await db.insert('posts', post_data)

    async def test_insert_and_delete_integer(self):
        async with self.async_db as db:
            data = {'integer_col': 123}
            row_id = await db.insert('data_types', data)
            self.assertIsNotNone(row_id, "Row ID should not be None after insertion")

            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 1, "Should return one row")
            self.assertEqual(rows[0]['integer_col'], 123, "The integer_col should be 123")

            await db.delete('data_types', 'id = ?', (row_id,))
            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 0, "No row should be returned after deletion")

    async def test_insert_and_delete_real(self):
        async with self.async_db as db:
            data = {'real_col': 123.456}
            row_id = await db.insert('data_types', data)
            self.assertIsNotNone(row_id, "Row ID should not be None after insertion")

            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 1, "Should return one row")
            self.assertEqual(rows[0]['real_col'], 123.456, "The real_col should be 123.456")

            await db.delete('data_types', 'id = ?', (row_id,))
            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 0, "No row should be returned after deletion")

    async def test_insert_and_delete_text(self):
        async with self.async_db as db:
            data = {'text_col': 'Sample text'}
            row_id = await db.insert('data_types', data)
            self.assertIsNotNone(row_id, "Row ID should not be None after insertion")

            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 1, "Should return one row")
            self.assertEqual(rows[0]['text_col'], 'Sample text', "The text_col should be 'Sample text'")

            await db.delete('data_types', 'id = ?', (row_id,))
            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 0, "No row should be returned after deletion")

    async def test_insert_and_delete_blob(self):
        async with self.async_db as db:
            data = {'blob_col': b'Sample blob'}
            row_id = await db.insert('data_types', data)
            self.assertIsNotNone(row_id, "Row ID should not be None after insertion")

            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 1, "Should return one row")
            self.assertEqual(rows[0]['blob_col'], b'Sample blob', "The blob_col should be 'Sample blob'")

            await db.delete('data_types', 'id = ?', (row_id,))
            rows = await db.select('data_types', where='id = ?', where_values=(row_id,))
            self.assertEqual(len(rows), 0, "No row should be returned after deletion")

if __name__ == "__main__":
    unittest.main()
