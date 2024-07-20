import pickle
from typing import Dict, Optional


class AccessFlags:
    __slots__ = ['_flags']

    DEFAULT_FLAGS: Dict = {
        'change_password': False, # Флаг, указывающий, может ли пользователь изменять пароли
        'change_access': False,   # Флаг, указывающий, может ли пользователь изменять уровни доступа
        'delete_users': False     # Флаг, указывающий, может ли пользователь удалять других пользователей
    }

    def __init__(self):
        """Инициализация объекта AccessFlags с флагами доступа по умолчанию.
        """
        self._flags: Dict = self.DEFAULT_FLAGS.copy()
    
    def set_flag(self, flag_name: str, value: bool) -> None:
        """Устанавливает значение заданного флага.

        Args:
            flag_name (str): Имя флага, значение которого необходимо изменить.
            value (bool): Новое значение флага.

        Raises:
            ValueError: Если флаг с заданным именем не существует.
        """
        if flag_name in self._flags:
            self._flags[flag_name] = value
        else:
            raise ValueError(f"Unknown flag: {flag_name}")
    
    def __getitem__(self, flag_name: str) -> Optional[bool]:
        """Возвращает значение заданного флага или None, если флаг не существует.

        Args:
            flag_name (str): Имя флага, значение которого необходимо получить.

        Returns:
            Optional[bool]: Текущее значение флага или None, если флаг не существует.
        """
        return self._flags.get(flag_name, None)
    
    def toggle_flag(self, flag_name: str) -> None:
        """Переключает значение заданного флага на противоположное.

        Args:
            flag_name (str): Имя флага, значение которого необходимо переключить.

        Raises:
            ValueError: Если флаг с заданным именем не существует.
        """
        if flag_name in self._flags:
            self._flags[flag_name] = not self._flags[flag_name]
        else:
            raise ValueError(f"Unknown flag: {flag_name}")

    def to_bytes(self) -> bytes:
        """Сериализует объект AccessFlags в байтовую строку.

        Returns:
            bytes: Сериализованный объект в виде байтовой строки.
        """
        return pickle.dumps(self)

    @staticmethod
    def from_bytes(binary_data: bytes) -> 'AccessFlags':
        """Десериализует объект AccessFlags из байтовой строки.

        Args:
            binary_data (bytes): Сериализованные данные в виде байтовой строки.

        Returns:
            AccessFlags: Десериализованный объект AccessFlags.
        """
        return pickle.loads(binary_data)

    @property
    def all_access(self) -> Dict[str, bool]:
        """Геттер на все доступы из класса.

        Returns:
            Dict[str, bool]: Словарь доступов.
        """
        return self._flags
    
    def __str__(self) -> str:
        """Возвращает строковое представление объекта AccessFlags.

        Returns:
            str: Строковое представление флагов доступа.
        """
        return str(self._flags)
