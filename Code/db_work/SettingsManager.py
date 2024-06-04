import asyncio
import json
import os

import aiofiles


class SettingsManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._path: str = os.path.join(os.getcwd(), 'Data', 'Settings', 'main_settings.json')
            self._initialized = True

    async def _create_file(self) -> bool:
        """
        Создание директории и файла, если они не были созданы ранее.
        
        Returns:
            bool: Возвращает True если файл был создан, иначе False
        
        Example:
        ```py
        settings_manager = SettingsManager()
        created = await settings_manager._create_file()
        print(created)  # True если файл был создан, иначе False
        ```
        """
        directory = os.path.dirname(self._path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._path):
            async with aiofiles.open(self._path, "w") as file:
                await file.write(json.dumps({}))
            return True
            
        return False

    async def load_settings(self) -> dict:
        """
        Загрузка настроек из файла.
        
        Returns:
            dict: Словарь с настройками
        
        Example:
        ```py
        settings_manager = SettingsManager()
        settings = await settings_manager.load_settings()
        print(settings)  # {'key': 'value'}
        ```
        """
        async with self._lock:
            if not os.path.exists(self._path):
                await self._create_file()

            async with aiofiles.open(self._path, "r") as file:
                content = await file.read()
                settings = json.loads(content)
        
        return settings

    async def save_settings(self, settings: dict) -> None:
        """
        Сохранение настроек в файл.
        
        Args:
            settings (dict): Словарь с настройками
        
        Example:
        ```py
        settings_manager = SettingsManager()
        await settings_manager.save_settings({'key': 'value'})
        ```
        """
        async with self._lock:
            async with aiofiles.open(self._path, "w") as file:
                await file.write(json.dumps(settings, indent=4))

    async def set_setting(self, key: str, value) -> None:
        """
        Устанавливает значение определенного поля в файле настроек.
        
        Args:
            key (str): Ключ поля
            value: Значение поля
        
        Example:
        ```py
        settings_manager = SettingsManager()
        await settings_manager.set_setting('bot.some_field.value', 'new_value')
        ```
        """
        async with self._lock:
            settings = await self.load_settings()
            keys = key.split('.')
            d = settings
           
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            
            d[keys[-1]] = value
            
            await self.save_settings(settings)

    async def get_setting(self, key: str):
        """
        Получает значение определенного поля из файла настроек.
        
        Args:
            key (str): Ключ поля
        
        Returns:
            Значение поля или None, если ключ не найден
        
        Example:
        ```py
        settings_manager = SettingsManager()
        value = await settings_manager.get_setting('bot.some_field.value')
        print(value)  # 'new_value' или None, если ключ не найден
        ```
        """
        async with self._lock:
            settings = await self.load_settings()
            keys = key.split('.')
            d = settings
            
            for k in keys:
                if k in d:
                    d = d[k]
                else:
                    return None
            
            return d
