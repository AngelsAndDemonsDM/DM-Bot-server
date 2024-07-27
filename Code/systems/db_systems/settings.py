import atexit
import json
import os
from typing import Any, Optional

from root_path import ROOT_PATH
from systems.decorators import global_class


class SettingsManager:
    __slots__ = ['_path', '_settings']

    def __init__(self, file_name: str = "NotSet") -> None:
        """Инициализирует менеджер настроек.

        Args:
            file_name (str): Имя файла настроек.
        
        Example::
        
            settings_manager = SettingsManager.get_instance()
        """
        self._path: str = os.path.join(ROOT_PATH, 'data', 'settings' f'{file_name}.json')
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

        Example::
        
            settings_manager.set_setting("user.preferences.theme", "dark")
        """
        keys = key.split('.')
        d = self._settings

        for k in keys[:-1]:
            d = d.setdefault(k, {})

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
        d = self._settings
        for k in key.split('.'):
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return default
        return d

    def initialize_default_settings(self, default_settings: dict) -> bool:
        """Инициализирует базовые настройки и сохраняет их в файл, если они не установлены.

        Args:
            default_settings (dict): Словарь с базовыми настройками.

        Returns:
            bool: Возвращает True, если инициализация произошла, иначе False.
        
        Example::
        
            default_settings = {
                "user.preferences.theme": "light",
                "app.language": "en",
                "app.version": "1.0.0"
            }
            settings_manager.initialize_default_settings(default_settings)
        """
        initialized = False
        for key, value in default_settings.items():
            if self.get_setting(key) is None:
                self.set_setting(key, value)
                initialized = True
        
        if initialized:
            self._save_settings()
        
        return initialized

    def __enter__(self):
        """Контекстный менеджер вход."""
        self._settings = self._load_settings()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Контекстный менеджер выход."""
        self._save_settings()

@global_class
class MainSettings(SettingsManager):
    def __init__(self) -> None:
        super().__init__("main_app")
