import hashlib
import hmac
import uuid
from typing import Tuple

from systems.access_system.access_flags import AccessFlags
from systems.db_systems import AsyncDB


class AuthError(Exception): # TODO: Заменить value error на эту ошибку
    """Общая ошибка выбрасываемая при ошибке получения доступа
    """
    pass

class AuthManager:
    __slots__ = ['_db']

    def __init__(self) -> None:
        """Инициализирует объект AuthManager и настраивает базу данных с двумя таблицами: 
        cur_sessions для хранения текущих сессий и users для хранения информации о пользователях.
        """
        self._db: AsyncDB = AsyncDB(
            file_name="auth",
            file_path="",
            config= { 
                "users": [ 
                    ("login", str, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None), 
                    ("password", str, (AsyncDB.NOT_NULL), None),
                    ("salt", str, (AsyncDB.NOT_NULL), None),
                    ("access", bytes, 0, None)
                ],
                "cur_sessions": [
                    ("token", str, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None),
                    ("user", str, (AsyncDB.NOT_NULL | AsyncDB.FOREIGN_KEY), "forkey|users.login|")
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
    def _compare_passwords(first_password: str, second_password: str) -> bool:
        """Сравнивает первый пароль со вторым паролем.

        Args:
            first_password (str): Первый пароль.
            second_password (str): Второй пароль.

        Returns:
            bool: True, если пароли совпадают, иначе False.
        """
        return hmac.compare_digest(first_password, second_password)

    @staticmethod
    def _generate_token() -> str:
        """Генерирует токен.
        Данный токен используется и как соль, и как токен аутентификации.

        Returns:
            str: Сгенерированный токен.
        """
        return uuid.uuid4().hex

    async def login_user(self, login: str, password: str) -> str:
        """Функция авторизации в системе.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.

        Raises:
            ValueError: В случае ненайденного пользователя или неверного пароля.

        Returns:
            str: Токен, под которым подключился пользователь.
        """
        async with self._db as db:
            data = await db.select('users', ['login', 'password', 'salt'], {'login': login})
        
        if not data:
            raise ValueError(f"User '{login}' not found")
        
        data = data[0]
        
        if not AuthManager._compare_passwords(
                str(data['password']),
                AuthManager._get_encrypted_password(password, data['salt'])
            ):
            raise ValueError("Password is incorrect")
        
        token: str = AuthManager._generate_token()
        async with self._db as db:
            await db.insert('cur_sessions', {
                'token': token,
                'user': login
            })
        
        return token
    
    async def logout_user(self, token: str) -> None:
        """Функция выхода пользователя из системы.

        Args:
            token (str): Токен пользователя.

        Raises:
            ValueError: В случае ненайденного токена.
        """
        async with self._db as db:
            session_data = await db.select('cur_sessions', ['user'], {'token': token})
            
            if not session_data:
                raise ValueError(f"Session with token '{token}' not found")
            
            await db.delete('cur_sessions', {'token': token})
    
    async def register_user(self, login: str, password: str, access: AccessFlags = None) -> str:
        """Регистрация нового пользователя.

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.
            access (AccessFlags, optional): Уровень доступа. По умолчанию None.

        Returns:
            str: Токен для новой зарегистрированной сессии.
        """
        salt = AuthManager._generate_token()
        encrypted_password = AuthManager._get_encrypted_password(password, salt)
        
        token: str = AuthManager._generate_token()
        
        if not access:
            access = AccessFlags()
        
        async with self._db as db:
            await db.insert('users', {
                'login': login,
                'password': encrypted_password,
                'salt': salt,
                'access': access.to_bytes()
            })
        
            await db.insert('cur_sessions', {
                'token': token,
                'user': login
            })
        
        return token
    
    async def delete_user(self, login: str) -> None:
        """Удаление пользователя из системы.

        Args:
            login (str): Логин пользователя.
        """
        async with self._db as db:
            await db.delete('cur_sessions', {'user': login})
            await db.delete('users', {'login': login})
    
    async def change_user_password(self, login: str, new_password: str) -> None:
        """Изменение пароля пользователя.

        Args:
            login (str): Логин пользователя.
            new_password (str): Новый пароль пользователя.
        """
        salt = AuthManager._generate_token()
        encrypted_password = AuthManager._get_encrypted_password(new_password, salt)
        
        async with self._db as db:
            await db.update('users', {'password': encrypted_password, 'salt': salt}, {'login': login})
    
    async def change_user_access(self, login: str, new_access: AccessFlags) -> None:
        """Изменение уровня доступа пользователя.

        Args:
            login (str): Логин пользователя.
            new_access (AccessFlags): Новый уровень доступа пользователя.
        """
        async with self._db as db:
            await db.update('users', {'access': new_access.to_bytes()}, {'login': login})

    async def get_user_access_by_token(self, token: str) -> AccessFlags:
        """Получение уровня доступа пользователя по токену.

        Args:
            token (str): Токен пользователя.

        Raises:
            ValueError: В случае ненайденного токена или пользователя.

        Returns:
            AccessFlags: Уровень доступа пользователя.
        """
        async with self._db as db:
            session_data = await db.select('cur_sessions', ['user'], {'token': token})
            
            if not session_data:
                raise ValueError(f"Session with token '{token}' not found")
            
            user_login = session_data[0]['user']
            
            user_data = await db.select('users', ['access'], {'login': user_login})
            
        if not user_data:
            raise ValueError(f"User '{user_login}' not found")
        
        return AccessFlags.from_bytes(user_data[0]['access'])

    async def get_user_access_by_login(self, login: str) -> AccessFlags:
        """Получение уровня доступа пользователя по логину.

        Args:
            login (str): Токен пользователя.

        Raises:
            ValueError: В случае ненайденного токена или пользователя.

        Returns:
            AccessFlags: Уровень доступа пользователя.
        """
        async with self._db as db:
            user_data = await db.select('users', ['access'], {'login': login})
            
        if not user_data:
            raise ValueError(f"User '{login}' not found")
        
        return AccessFlags.from_bytes(user_data[0]['access'])

    async def get_user_login_by_token(self, token: str) -> str:
        """Получение логина пользователя по токену.

        Args:
            token (str): Токен пользователя.

        Raises:
            ValueError: В случае ненайденного токена или пользователя.

        Returns:
            str: Логин пользователя.
        """
        async with self._db as db:
            session_data = await db.select('cur_sessions', ['user'], {'token': token})
            
        if not session_data:
            raise ValueError(f"Session with token '{token}' not found")
        
        return session_data[0]['user']

    async def get_user_login_and_access_by_token(self, token: str) -> Tuple[str, AccessFlags]:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            Tuple[AccessFlags, str]: _description_
        """
        async with self._db as db:
            session_data = await db.select('cur_sessions', ['user'], {'token': token})
            
            if not session_data:
                raise ValueError(f"Session with token '{token}' not found")
            
            user_login = session_data[0]['user']
            
            user_data = await db.select('users', ['access'], {'login': user_login})
            
        if not user_data:
            raise ValueError(f"User '{user_login}' not found")
        
        return (user_login, AccessFlags.from_bytes(user_data[0]['access']))