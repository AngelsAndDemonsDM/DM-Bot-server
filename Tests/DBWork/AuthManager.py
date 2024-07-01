import hashlib
import hmac
import unittest

from Code.db_work import AuthManager


class AsyncMockDB:
    def __init__(self):
        self.data = {
            "users": [],
            "cur_sessions": []
        }

    async def insert(self, table, values):
        self.data[table].append(values)

    async def select(self, table, columns, where_clause, where_args):
        if table == "users":
            for user in self.data["users"]:
                if user["login"] == where_args[0]:
                    return [user]
        if table == "cur_sessions":
            for session in self.data["cur_sessions"]:
                if session["token"] == where_args[0]:
                    return [session]
        return []

    async def delete(self, table, where_clause, where_args):
        if table == "cur_sessions":
            for session in self.data["cur_sessions"]:
                if session["token"] == where_args[0]:
                    self.data["cur_sessions"].remove(session)
                    return 1
        return 0

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.auth_manager = AuthManager()
        self.auth_manager._db = AsyncMockDB()

    def test_get_encrypted_password(self):
        password = "test_password"
        salt = "test_salt"
        encrypted_password = self.auth_manager._get_encrypted_password(password, salt)
        expected_password = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
        self.assertEqual(encrypted_password, expected_password)

    def test_compare_passwords(self):
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
        
        user = self.auth_manager._db.data["users"][0]
        self.assertEqual(user["login"], login)
        self.assertEqual(user["access"], access)

    async def test_authentication_success(self):
        login = "test_user"
        password = "test_password"
        salt = "test_salt"
        access = b'\x01'
        encrypted_password = self.auth_manager._get_encrypted_password(password, salt)
        
        await self.auth_manager._db.insert("users", {"login": login, "password": encrypted_password, "salt": salt, "access": access})

        token = await self.auth_manager.authentication(login, password)
        self.assertIsNotNone(token)
        session = self.auth_manager._db.data["cur_sessions"][0]
        self.assertEqual(session["access"], access)

    async def test_authentication_failure(self):
        login = "test_user"
        password = "test_password"

        token = await self.auth_manager.authentication(login, password)
        self.assertIsNone(token)

    async def test_get_token_access(self):
        token = "test_token"
        access = b'\x01'

        await self.auth_manager._db.insert("cur_sessions", {"token": token, "access": access})

        result = await self.auth_manager.get_token_access(token)
        self.assertEqual(result, access)

    async def test_logout(self):
        token = "test_token"
        access = b'\x01'

        await self.auth_manager._db.insert("cur_sessions", {"token": token, "access": access})

        result = await self.auth_manager.logout(token)
        self.assertTrue(result)
        self.assertEqual(len(self.auth_manager._db.data["cur_sessions"]), 0)

if __name__ == '__main__':
    unittest.main()
