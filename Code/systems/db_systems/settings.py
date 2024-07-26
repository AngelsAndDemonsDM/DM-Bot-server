import atexit
import json
import os
from functools import reduce
from typing import Any, Optional

from root_path import ROOT_PATH


class SettingsManager:
    __slots__ = ['_path', '_settings']

    def __init__(self, settings_name: str = "main_settings") -> None:
        """Инициализирует менеджер настроек.

        Args:
            settings_name (str, optional): Имя файла настроек. Defaults to "main_settings".

        Example:
        ```py
        settings_manager = SettingsManager("app_settings")
        ```
        """
        self._path: str = os.path.join(ROOT_PATH, 'data', 'settings', f'{settings_name}.json')
        self._settings: dict = self._load_settings()
        atexit.register(self._save_settings)

    def _create_file(self) -> bool:
        """Создает файл настроек, если он не существует.

        Returns:
            bool: Возвращает True, если файл был создан, иначе False.
        """
        directory = os.path.dirname(self._path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._path):
            with open(self._path, "w") as file:
                file.write(json.dumps({}))

            return True

        return False

    def _load_settings(self) -> dict:
        """Загружает настройки из файла."""
        self._create_file()

        if os.path.getsize(self._path) > 0:
            with open(self._path, "r") as file:
                return json.load(file)
        else:
            return {}

    def _save_settings(self) -> None:
        """Сохраняет настройки в файл."""
        with open(self._path, "w") as file:
            file.write(json.dumps(self._settings, indent=4))

    def set_setting(self, key: str, value: Any) -> None:
        """Устанавливает значение настройки.

        Args:
            key (str): Ключ настройки, поддерживается вложенность через точку (например, "user.preferences.theme").
            value (Any): Значение настройки.

        Example:
        ```py
        settings_manager.set_setting("user.preferences.theme", "dark")
        ```
        """
        keys = key.split('.')
        d = self._settings

        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]

        d[keys[-1]] = value

    def get_setting(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Получает значение настройки.

        Args:
            key (str): Ключ настройки, поддерживается вложенность через точку (например, "user.preferences.theme").
            default (Optional[Any]): Значение по умолчанию, если ключ не найден.

        Returns:
            Optional[Any]: Значение настройки или значение по умолчанию, если ключ не найден.

        Example::
        
            theme = settings_manager.get_setting("user.preferences.theme")
            print(theme)  # "dark"
        """
        try:
            return reduce(lambda d, k: d[k], key.split('.'), self._settings)
        
        except KeyError:
            return default

    def __enter__(self):
        """Контекстный менеджер вход."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Контекстный менеджер выход."""
        self._save_settings()
