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
            self._queue: asyncio.Queue = asyncio.Queue()
            self._task = None
            self._initialized = True

    async def start(self):
        async with self._lock:
            if self._task is None:
                self._task = asyncio.create_task(self._process_queue())

    async def stop(self):
        async with self._lock:
            if self._task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
                self._task = None

    async def _create_file(self) -> bool:
        """Создание директории и файла, если они не были созданы ранее.
        
        Returns:
            bool: Возвращает True если файл был создан, иначе False
        """
        directory = os.path.dirname(self._path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._path):
            async with aiofiles.open(self._path, "w") as file:
                await file.write(json.dumps({}))
            return True
            
        return False

    async def _process_queue(self):
        while True:
            func, args, kwargs, future = await self._queue.get()
            try:
                result = await func(*args, **kwargs)
                future.set_result(result)
            except Exception as err:
                future.set_exception(err)
            finally:
                self._queue.task_done()

    async def load_settings(self) -> dict:
        """Загрузка настроек из файла.
        
        Returns:
            dict: Словарь с настройками
        """
        future = asyncio.Future()
        await self._queue.put((self._load_settings, [], {}, future))
        return await future

    async def _load_settings(self) -> dict:
        """Реальная загрузка настроек из файла. Эта функция вызывается из очереди.
        
        Returns:
            dict: Словарь с настройками
        """
        if not os.path.exists(self._path):
            await self._create_file()
        
        async with aiofiles.open(self._path, "r") as file:
            content = await file.read()
            settings = json.loads(content)
        
        return settings

    async def save_settings(self, settings: dict) -> None:
        """Сохранение настроек в файл.
        
        Args:
            settings (dict): Словарь с настройками
        """
        future = asyncio.Future()
        await self._queue.put((self._save_settings, [settings], {}, future))
        await future

    async def _save_settings(self, settings: dict) -> None:
        """Реальное сохранение настроек в файл. Эта функция вызывается из очереди.
        
        Args:
            settings (dict): Словарь с настройками
        """
        async with aiofiles.open(self._path, "w") as file:
            await file.write(json.dumps(settings, indent=4))

    async def set_setting(self, key: str, value) -> None:
        """Устанавливает значение определенного поля в файле настроек.
        
        Args:
            key (str): Ключ поля
            value: Значение поля
        """
        future = asyncio.Future()
        await self._queue.put((self._set_setting, [key, value], {}, future))
        await future

    async def _set_setting(self, key: str, value) -> None:
        """Реальная установка значения определенного поля в файле настроек. Эта функция вызывается из очереди.
        
        Args:
            key (str): Ключ поля
            value: Значение поля
        """
        settings = await self._load_settings()
        settings[key] = value
        await self._save_settings(settings)

    async def get_setting(self, key: str):
        """Получает значение определенного поля из файла настроек.
        
        Args:
            key (str): Ключ поля
        
        Returns:
            Значение поля или None, если ключ не найден
        """
        future = asyncio.Future()
        await self._queue.put((self._get_setting, [key], {}, future))
        return await future

    async def _get_setting(self, key: str):
        """Реальное получение значения определенного поля из файла настроек. Эта функция вызывается из очереди.
        
        Args:
            key (str): Ключ поля
        
        Returns:
            Значение поля или None, если ключ не найден
        """
        settings = await self._load_settings()
        return settings.get(key, None)
