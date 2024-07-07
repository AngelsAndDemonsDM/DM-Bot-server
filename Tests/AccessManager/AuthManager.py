import os
import unittest

from Code.systems.access_manager import AuthManager


class TestAuthManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.auth_manager = AuthManager()
        
    async def asyncTearDown(self):
        if os.path.exists(self.auth_manager._db._file_path):
            os.remove(self.auth_manager._db._file_path)

    async def test_register_user(self):
        token = await self.auth_manager.register_user('testuser', 'testpassword')
        self.assertIsNotNone(token)
        async with self.auth_manager._db as db:
            user_data = await db.select('users', ['login', 'password', 'salt'], {'login': 'testuser'})
        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['login'], 'testuser')

    async def test_login_user(self):
        await self.auth_manager.register_user('testuser', 'testpassword')
        token = await self.auth_manager.login_user('testuser', 'testpassword')
        self.assertIsNotNone(token)

    async def test_login_user_invalid_password(self):
        await self.auth_manager.register_user('testuser', 'testpassword')
        with self.assertRaises(ValueError):
            await self.auth_manager.login_user('testuser', 'wrongpassword')

    async def test_logout_user(self):
        token = await self.auth_manager.register_user('testuser', 'testpassword')
        await self.auth_manager.logout_user(token)
        async with self.auth_manager._db as db:
            session_data = await db.select('cur_sessions', ['token'], {'token': token})
        self.assertEqual(len(session_data), 0)

    async def test_delete_user(self):
        await self.auth_manager.register_user('testuser', 'testpassword')
        await self.auth_manager.delete_user('testuser')
        async with self.auth_manager._db as db:
            user_data = await db.select('users', ['login'], {'login': 'testuser'})
        self.assertEqual(len(user_data), 0)

    async def test_change_user_password(self):
        await self.auth_manager.register_user('testuser', 'testpassword')
        await self.auth_manager.change_user_password('testuser', 'newpassword')
        token = await self.auth_manager.login_user('testuser', 'newpassword')
        self.assertIsNotNone(token)

    async def test_change_user_access(self):
        await self.auth_manager.register_user('testuser', 'testpassword')
        await self.auth_manager.change_user_access('testuser', b'\x01')
        async with self.auth_manager._db as db:
            user_data = await db.select('users', ['access'], {'login': 'testuser'})
        self.assertEqual(user_data[0]['access'], b'\x01')

    async def test_get_user_access(self):
        token = await self.auth_manager.register_user('testuser', 'testpassword', b'\x02')
        access = await self.auth_manager.get_user_access(token)
        self.assertEqual(access, b'\x02')

    async def test_get_user_login(self):
        token = await self.auth_manager.register_user('testuser', 'testpassword', b'\x02')
        login = await self.auth_manager.get_user_login(token)
        self.assertEqual(login, 'testuser')

if __name__ == '__main__':
    unittest.main()
