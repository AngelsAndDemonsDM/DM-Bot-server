import asyncio
import hashlib
import os
import pickle

import aiofiles


class FileWork:
    def __init__(self, path):
        path = os.path.dirname(path)
        self.path = os.path.join(os.getcwd(), '..', 'data', path)
        self.data = None
        self.cached = False
        self.file_hash = None
        self.lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if cls is FileWork:
            raise TypeError("You cannot create an abstract 'FileWork' class. Use inheritance")
        return super().__new__(cls)

    async def create_file(self):
        """
        Создание директории и файла, если оно не было создано уже
        
        Args:
            None
        
        Returns:
            None
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    async def _calculate_file_hash(self):
        """
        Рассчитывает хеш файла
        
        Args:
            None
        
        Returns:
            str: Хеш файла
        """
        hasher = hashlib.sha256()
        async with aiofiles.open(self.path, 'rb') as file:
            while chunk := await file.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    async def _load_file(self):
        """
        Загрузка данных с файла
            
        Args:
            None
            
        Returns:
            data (DataFiles): Загруженный файл данных
        """
        try:
            async with aiofiles.open(self.path, 'rb') as file:
                return pickle.loads(await file.read())
        except Exception as e:
            print(f"An error occurred in {self.path}: {e}")
            return None

    async def load_data(self):
        """
        Загрузка данных с использованием кэширования и проверки хеша файла
        
        Args:
            None
        
        Returns:
            data (DataFiles): Загруженный файл данных
        """
        async with self.lock:
            current_hash = await self._calculate_file_hash()
            if not self.cached or self.file_hash != current_hash:
                self.data = await self._load_file()
                self.cached = True
                self.file_hash = current_hash
        return self.data

    async def _save_file(self):
        """
        Сохранение данных на файл
        
        Args:
            None
        
        Returns:
            None
        """
        if self.data is not None:
            async with aiofiles.open(self.path, 'wb') as file:
                await file.write(pickle.dumps(self.data))
        else:
            print("No data to save.")

    async def save_data(self):
        """
        Сохранение данных
        
        Args:
            None
        
        Returns:
            None
        """
        async with self.lock:
            await self._save_file()
            self.cached = False
