import hashlib
import hmac
import uuid
from typing import Optional, Tuple

from db_work.AsyncDB import AsyncDB


class AuthManager:
    __slots__ = ['_db']

    def __init__(self) -> None:
        """Инициализирует объект AuthManager и настраивает базу данных с двумя таблицами: 
        cur_sessions для хранения текущих сессий и users для хранения информации о пользователях.
        """
        self._db: AsyncDB = AsyncDB(
            db_name="auth",
            db_path="data",
            db_config= { 
                "users": [ 
                    ("login", str, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None), 
                    ("password", str, 0, None),
                    ("salt", str, 0, None),
                    ("access", bytes, 0, None)
                ],

                "cur_sessions": [
                    ("token", str, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None),
                    ("login", str, (AsyncDB.UNIQUE), "users.login"),
                    ("access", bytes, 0, "users.access")
                ]
            }
        )

    @staticmethod
    def _get_encrypted_password(password: str, salt: str) -> str:
        """Хэширует пароль с использованием соли.

        Args:
            password (str): Пароль пользователя.
            salt (str): Соль для хэширования.

        Returns:
            str: Хэшированный пароль.
        """
        return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def _compare_passwords(stored_password: str, provided_password: str, salt: str) -> bool:
        """Сравнивает хэшированный пароль из базы данных с предоставленным паролем.

        Args:
            stored_password (str): Хэшированный пароль, хранящийся в базе данных.
            provided_password (str): Пароль, предоставленный пользователем.
            salt (str): Соль для хэширования.

        Returns:
            bool: True, если пароли совпадают, иначе False.
        """
        encrypted_password = AuthManager._get_encrypted_password(provided_password, salt)
        return hmac.compare_digest(stored_password, encrypted_password)

    async def _generate_access_token(self, login: str, access: bytes) -> str:
        """Генерирует уникальный токен доступа и сохраняет его вместе с доступом в таблице cur_sessions.

        Args:
            access (bytes): Флаги доступа для сессии.

        Returns:
            str: Сгенерированный токен доступа.
        """
        random_uuid = uuid.uuid4().hex
        async with self._db as db:
            await db.insert("cur_sessions", {"token": random_uuid, "login": login, "access": access})
        
        return random_uuid

    async def register_user(self, login: str, password: str, access: bytes = b'\x00') -> str:
        """Регистрирует нового пользователя с заданным логином, паролем и флагами доступа. 
        Также генерирует и возвращает токен доступа для нового пользователя.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.
            access (bytes, optional): Флаги доступа. По умолчанию b'\x00'.

        Returns:
            str: Токен доступа для нового пользователя.
        """
        salt = uuid.uuid4().hex
        
        encrypted_password = AuthManager._get_encrypted_password(password, salt)
        async with self._db as db:
            await db.insert("users", {"login": login, "password": encrypted_password, "salt": salt, "access": access})
        
        return await self._generate_access_token(login, access)

    async def get_token_info(self, token: str) -> Optional[Tuple[str, bytes]]:
        """Возвращает информацию о токене доступа. Его права и логин кому принадлежит

        Args:
            token (str): Токен доступа

        Returns:
            Optional[Tuple[str, bytes]]: Логин и права.
        """
        async with self._db as db:
            token_info = await db.select("cur_sessions", ["login", "access"], "token = ?", (token,))
        
        if token_info:
            return (token_info[0]['login'], token_info[0]['access'])
        
        return None

    async def logout(self, token: str) -> None:
        """Удаляет сессию, связанную с заданным токеном.

        Args:
            token (str): Токен доступа.
        """
        async with self._db as db:
            await db.delete("cur_sessions", "token = ?", (token,))
            
    async def login(self, login: str, password: str) -> Optional[str]:
        """Аутентифицирует пользователя по логину и паролю. При успешной аутентификации генерирует токен доступа.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.

        Returns:
            Optional[str]: Токен доступа при успешной аутентификации, иначе None.
        """
        get_access: bool = False
        user_access: Optional[bytes] = None
        
        async with self._db as db:
            user = await db.select("users", ["login", "password", "salt", "access"], "login = ?", (login,))
        
        if user:
            stored_password = user[0]['password']
            salt = user[0]['salt']
            if AuthManager._compare_passwords(stored_password, password, salt):
                get_access = True
                user_access = user[0]['access']

        if get_access:
            return await self._generate_access_token(login, user_access)
        
        return None

    async def change_password(self, login: str, new_password: str) -> None:
        """Метод позволяет сменить пароль у пользователя

        Args:
            login (str): Логин пользователя
            new_password (str): Новый пароль
        """
        salt = uuid.uuid4().hex
        
        encrypted_password = AuthManager._get_encrypted_password(new_password, salt)
        async with self._db as db:
            await db.update('users', {'password': encrypted_password, 'salt': salt}, 'login = ?', (login,))

    async def delete_user(self, login: str) -> None:
        """Метод позволяет удалить данные о пользователе.

        Args:
            login (str): Логин который надо удалить
        """
        async with self._db as db:
            await db.delete('users', 'login = ?', (login,))
            await db.delete('cur_sessions', 'login = ?', (login,))
