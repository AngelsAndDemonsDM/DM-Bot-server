import hashlib
import hmac
import os
import unittest

from Code.access_manager import AuthManager


class TestAuthManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.auth_manager = AuthManager()

    async def asyncTearDown(self):
        if os.path.exists(self.auth_manager._db._db_path):
            os.remove(self.auth_manager._db._db_path)

    async def test_get_encrypted_password(self):
        password = "test_password"
        salt = "test_salt"
        encrypted_password = self.auth_manager._get_encrypted_password(password, salt)
        expected_password = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
        self.assertEqual(encrypted_password, expected_password)

    async def test_compare_passwords(self):
        password = "test_password"
        salt = "test_salt"
        encrypted_password = self.auth_manager._get_encrypted_password(password, salt)
        result = self.auth_manager._compare_passwords(encrypted_password, password, salt)
        self.assertTrue(result)

    async def test_register_user(self):
        login = "test_user"
        password = "test_password"
        access = b'\x01'

        token = await self.auth_manager.register_user(login, password, access)
        
        async with self.auth_manager._db as db:
            user = await db.select("users", ["login", "access"], "login = ?", (login,))
        
        self.assertEqual(user[0]["login"], login)
        self.assertEqual(user[0]["access"], access)

    async def test_authentication_success(self):
        login = "test_user"
        password = "test_password"
        salt = "test_salt"
        access = b'\x01'
        encrypted_password = self.auth_manager._get_encrypted_password(password, salt)

        async with self.auth_manager._db as db:
            await db.insert("users", {"login": login, "password": encrypted_password, "salt": salt, "access": access})

        token = await self.auth_manager.login(login, password)
        self.assertIsNotNone(token)
        
        async with self.auth_manager._db as db:
            session = await db.select("cur_sessions", ["access"], "token = ?", (token,))
        
        self.assertEqual(session[0]["access"], access)

    async def test_authentication_failure(self):
        login = "test_user"
        password = "test_password"

        token = await self.auth_manager.login(login, password)
        self.assertIsNone(token)

    async def test_get_token_access(self):
        token = "test_token"
        login = "test_user"
        access = b'\x01'

        async with self.auth_manager._db as db:
            await db.insert("cur_sessions", {"token": token, "access": access, "login": login})

        get_login, get_access = await self.auth_manager.get_token_info(token)
        self.assertEqual(get_login, login)
        self.assertEqual(get_access, access)

    async def test_logout(self):
        token = "test_token"
        access = b'\x01'

        async with self.auth_manager._db as db:
            await db.insert("cur_sessions", {"token": token, "access": access})

        await self.auth_manager.logout(token)
        
        async with self.auth_manager._db as db:
            session = await db.select("cur_sessions", ["token"], "token = ?", (token,))
        
        self.assertEqual(len(session), 0)

if __name__ == '__main__':
    unittest.main()
