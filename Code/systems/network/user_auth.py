import uuid
from typing import Dict, Optional, Tuple

import bcrypt
import msgpack
from systems.db_systems import AsyncDB


# --- Access systems --- #
class UserAccess:
    __slots__ = ['_flags']
    DEFAULT_FLAGS: Dict[str, bool] = {
        "something": False,  # Тестовый флаг доступа.
    }

    def __init__(self) -> None:
        self._flags: Dict[str, bool] = UserAccess.DEFAULT_FLAGS.copy()

    # --- set/get flag --- #
    def get_flag(self, key: str) -> Optional[bool]:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            Optional[bool]: _description_
        """
        return self._flags.get(key, None)

    def set_flag(self, key: str, value: bool) -> None:
        """_summary_

        Args:
            key (str): _description_
            value (bool): _description_

        Raises:
            ValueError: _description_
        """
        if key not in UserAccess.DEFAULT_FLAGS:
            raise ValueError(f"key '{key}' is not an access flag")
        
        self._flags[key] = value

    # --- bytes work --- #
    @staticmethod
    def restore(data: bytes) -> 'UserAccess':
        """_summary_

        Args:
            data (bytes): _description_

        Returns:
            UserAccess: _description_
        """
        unpacked_data = msgpack.unpackb(data, raw=False)
        user_access = UserAccess()
        user_access._flags = unpacked_data['_flags']
        return user_access

    def dump(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return msgpack.packb({'_flags': self._flags})


# --- auth systems --- #
class AuthError(Exception):
    """Ошибка вызываемая в случае если пользователь отсутствует или пароль не верен"""
    pass


class UserAuth:
    __slots__ = ['_db']

    def __init__(self) -> None:
        """_summary_
        """
        self._db = AsyncDB(
            file_name="user_auth",
            file_path="",
            config={
                'users': [
                    ('login', str, AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE, None),
                    ('password', bytes, 0, None),
                    ('access', bytes, AsyncDB.NOT_NULL, None)
                ],
                'session': [
                    ('token', str, 0, None),
                    ('user', str, AsyncDB.FOREIGN_KEY, 'forkey|users.login|')
                ]}
        )

    # --- Magic --- #
    @staticmethod
    def _hash_password(password: str) -> bytes:
        """_summary_

        Args:
            password (str): _description_

        Returns:
            bytes: _description_
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def _check_password(password: str, hashed: bytes) -> bool:
        """_summary_

        Args:
            password (str): _description_
            hashed (bytes): _description_

        Returns:
            bool: _description_
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    @staticmethod
    def _create_token() -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return str(uuid.uuid4())

    # --- User control --- #
    async def register_user(self, login: str, password: str) -> None:
        """_summary_

        Args:
            login (str): _description_
            password (str): _description_
        """
        hash_password = UserAuth._hash_password(password)
        access = UserAccess()

        async with self._db as db:
            await db.insert("users", {'login': login, 'password': hash_password, 'access': access.dump()})

    async def login_user(self, login: str, password: str) -> str:
        """_summary_

        Args:
            login (str): _description_
            password (str): _description_

        Raises:
            AuthError: _description_
            AuthError: _description_

        Returns:
            str: _description_
        """
        async with self._db as db:
            data = await db.select("users", ["password"], {"login": login})

        if not data:
            raise AuthError(f"User '{login}' not found")

        if UserAuth._check_password(password, data[0]["password"]):
            token = UserAuth._create_token()
            async with self._db as db:
                await db.insert("session", {'token': token, 'user': login})
            
            return token
        
        raise AuthError("Incorrect password")

    async def delete_user(self, login: str) -> None:
        """_summary_

        Args:
            login (str): _description_
        """
        async with self._db as db:
            await db.delete("users", {"login": login})

    async def change_password(self, login: str, new_password: str) -> None:
        """_summary_

        Args:
            login (str): _description_
            new_password (str): _description_
        """
        hash_password = UserAuth._hash_password(new_password)
        async with self._db as db:
            await db.update("users", {"password": hash_password}, {"login": login})

    async def change_access(self, login: str, new_access: UserAccess) -> None:
        """_summary_

        Args:
            login (str): _description_
            new_access (UserAccess): _description_
        """
        async with self._db as db:
            await db.update("users", {"access": new_access.dump()}, {"login": login})

    # --- Get by token --- #
    async def get_login_by_token(self, token: str) -> str:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            AuthError: _description_

        Returns:
            str: _description_
        """
        async with self._db as db:
            data = await db.select("session", ["user"], {"token": token})
        
        if not data:
            raise AuthError(f"Session token '{token}' not found")
        
        return data[0]["user"]

    async def get_access_by_token(self, token: str) -> UserAccess:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            AuthError: _description_
            AuthError: _description_

        Returns:
            UserAccess: _description_
        """
        async with self._db as db:
            data = await db.select("session", ["user"], {"token": token})
            
            if not data:
                raise AuthError(f"Session token '{token}' not found")
            
            login = data[0]["user"]
            user_data = await db.select("users", ["access"], {"login": login})
            
            if not user_data:
                raise AuthError(f"User '{login}' not found")
            
            return UserAccess.restore(user_data[0]["access"])

    async def get_login_access_by_token(self, token: str) -> Tuple[str, UserAccess]:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            AuthError: _description_
            AuthError: _description_

        Returns:
            Tuple[str, UserAccess]: _description_
        """
        async with self._db as db:
            data = await db.select("session", ["user"], {"token": token})
            if not data:
                raise AuthError(f"Session token '{token}' not found")
            
            login = data[0]["user"]
            user_data = await db.select("users", ["access"], {"login": login})
            if not user_data:
                raise AuthError(f"User '{login}' not found")
            
            access = UserAccess.restore(user_data[0]["access"])
            return login, access

    # --- Get by login --- #
    async def get_access_by_login(self, login: str) -> UserAccess:
        """_summary_

        Args:
            login (str): _description_

        Raises:
            AuthError: _description_

        Returns:
            UserAccess: _description_
        """
        async with self._db as db:
            data = await db.select("users", ["access"], {"login": login})
        
        if not data:
            raise AuthError(f"User '{login}' not found")
        
        return UserAccess.restore(data[0]["access"])
