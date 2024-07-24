import uuid
from typing import Dict, Optional, Tuple

import bcrypt
import msgpack
from systems.db_systems import AsyncDB
from systems.singleton import singleton


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
        """Возвращает значение флага доступа по его ключу.

        Args:
            key (str): Ключ флага доступа.

        Returns:
            Optional[bool]: Значение флага доступа или None, если ключ не найден.
        """
        return self._flags.get(key, None)

    def set_flag(self, key: str, value: bool) -> None:
        """Устанавливает значение флага доступа по его ключу.

        Args:
            key (str): Ключ флага доступа.
            value (bool): Значение флага доступа.

        Raises:
            ValueError: Если ключ не является флагом доступа.
        """
        if key not in UserAccess.DEFAULT_FLAGS:
            raise ValueError(f"key '{key}' is not an access flag")
        
        self._flags[key] = value

    # --- bytes work --- #
    @staticmethod
    def restore(data: bytes) -> 'UserAccess':
        """Восстанавливает объект UserAccess из байтовых данных.

        Args:
            data (bytes): Байтовые данные.

        Returns:
            UserAccess: Восстановленный объект UserAccess.
        """
        unpacked_data = msgpack.unpackb(data, raw=False)
        user_access = UserAccess()
        user_access._flags = unpacked_data['_flags']
        return user_access

    def dump(self) -> bytes:
        """Сериализует объект UserAccess в байтовые данные.

        Returns:
            bytes: Сериализованные байтовые данные.
        """
        return msgpack.packb({'_flags': self._flags})


# --- auth systems --- #
class AuthError(Exception):
    """Ошибка вызываемая в случае если пользователь отсутствует или пароль не верен"""
    pass

@singleton
class UserAuth:
    __slots__ = ['_db']

    def __init__(self) -> None:
        """Инициализация UserAuth.

        Создает экземпляр класса UserAuth и инициализирует базу данных _db с таблицами "users" и "session".
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
        """Хеширует пароль.

        Args:
            password (str): Пароль пользователя.

        Returns:
            bytes: Захешированный пароль.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def _check_password(password: str, hashed: bytes) -> bool:
        """Проверяет соответствие пароля и хеша.

        Args:
            password (str): Пароль пользователя.
            hashed (bytes): Захешированный пароль.

        Returns:
            bool: True, если пароль соответствует хешу, иначе False.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    @staticmethod
    def _create_token() -> str:
        """Создает уникальный токен сессии.

        Returns:
            str: Сгенерированный токен сессии.
        """
        return str(uuid.uuid4())

    # --- User control --- #
    async def register_user(self, login: str, password: str) -> None:
        """Регистрирует нового пользователя.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.
        """
        hash_password = UserAuth._hash_password(password)
        access = UserAccess()

        async with self._db as db:
            await db.insert("users", {'login': login, 'password': hash_password, 'access': access.dump()})

    async def login_user(self, login: str, password: str) -> str:
        """Авторизует пользователя и создает сессию.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.

        Raises:
            AuthError: Если пользователь не найден.
            AuthError: Если пароль неверный.

        Returns:
            str: Токен сессии.
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
        """Удаляет пользователя.

        Args:
            login (str): Логин пользователя.
        """
        async with self._db as db:
            await db.delete("users", {"login": login})

    async def change_password(self, login: str, new_password: str) -> None:
        """Изменяет пароль пользователя.

        Args:
            login (str): Логин пользователя.
            new_password (str): Новый пароль пользователя.
        """
        hash_password = UserAuth._hash_password(new_password)
        async with self._db as db:
            await db.update("users", {"password": hash_password}, {"login": login})

    async def change_access(self, login: str, new_access: UserAccess) -> None:
        """Изменяет права доступа пользователя.

        Args:
            login (str): Логин пользователя.
            new_access (UserAccess): Новый уровень доступа пользователя.
        """
        async with self._db as db:
            await db.update("users", {"access": new_access.dump()}, {"login": login})

    # --- Get by token --- #
    async def get_login_by_token(self, token: str) -> str:
        """Получает логин пользователя по токену сессии.

        Args:
            token (str): Токен сессии.

        Raises:
            AuthError: Если токен не найден.

        Returns:
            str: Логин пользователя.
        """
        async with self._db as db:
            data = await db.select("session", ["user"], {"token": token})
        
        if not data:
            raise AuthError(f"Session token '{token}' not found")
        
        return data[0]["user"]

    async def get_access_by_token(self, token: str) -> UserAccess:
        """Получает права доступа пользователя по токену сессии.

        Args:
            token (str): Токен сессии.

        Raises:
            AuthError: Если токен не найден.
            AuthError: Если пользователь не найден.

        Returns:
            UserAccess: Права доступа пользователя.
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
        """Получает логин и права доступа пользователя по токену сессии.

        Args:
            token (str): Токен сессии.

        Raises:
            AuthError: Если токен не найден.
            AuthError: Если пользователь не найден.

        Returns:
            Tuple[str, UserAccess]: Логин и права доступа пользователя.
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
        """Получает права доступа пользователя по его логину.

        Args:
            login (str): Логин пользователя.

        Raises:
            AuthError: Если пользователь не найден.

        Returns:
            UserAccess: Права доступа пользователя.
        """
        async with self._db as db:
            data = await db.select("users", ["access"], {"login": login})
        
        if not data:
            raise AuthError(f"User '{login}' not found")
        
        return UserAccess.restore(data[0]["access"])
