import asyncio
import hashlib
import os
import pickle

import aiofiles


class FileWork:
    def __init__(self, file_path):
        """
        Инициализация объекта FileWork.

        Args:
            file_path (str): Путь к файлу.

        Attributes:
            path (str): Полный путь к файлу.
            data (object): Данные файла.
            cached (bool): Флаг указывающий, кэшированы ли данные.
            file_hash (str): Хэш файла.
            lock (asyncio.Lock): Асинхронный замок для обеспечения безопасности при доступе к данным из разных потоков.
        """
        self.path = os.path.join(os.getcwd(), 'Data.DM-Bot', file_path)
        self.data = None
        self.cached = False
        self.file_hash = None
        self.lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса FileWork.
        """
        if cls is FileWork:
            raise NotImplementedError(f"You cannot create an abstract '{self.__class__.__name__}' class. Use inheritance")
        return super().__new__(cls)

    async def create_file(self):
        """
        Создание директории и файла, если они не были созданы ранее.
        
        Returns:
            bool: Возвращает True если файл был создан, иначе False
        """
        directory = os.path.dirname(self.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.path):
            with open(self.path, "wb") as file:
                pickle.dump(None, file)
                return True
        
        return False

    async def _calculate_file_hash(self):
        """
        Рассчитывает хеш файла.

        Returns:
            str: Хеш файла.
        """
        hasher = hashlib.sha256()
        async with aiofiles.open(self.path, 'rb') as file:
            async for chunk in file:
                hasher.update(chunk)
        return hasher.hexdigest()

    async def _load_file(self):
        """
        Загрузка данных из файла.

        Returns:
            object: Данные файла.
        """
        try:
            async with aiofiles.open(self.path, 'rb') as file:
                return await file.read()
        except Exception as e:
            print(f"An error occurred in {self.path}: {e}")
            return None

    async def load_data(self):
        """
        Загрузка данных с использованием кэширования и проверки хеша файла.

        Returns:
            object: Загруженные данные файла.
        """
        async with self.lock:
            current_hash = await self._calculate_file_hash()
            if not self.cached or self.file_hash != current_hash:
                file_content = await self._load_file()
                if file_content is not None:
                    self.data = pickle.loads(file_content)
                    self.cached = True
                    self.file_hash = current_hash
        return self.data

    async def _save_file(self):
        """
        Сохранение данных в файл.
        """
        if self.data is not None:
            async with aiofiles.open(self.path, 'wb') as file:
                await file.write(pickle.dumps(self.data))
        else:
            print("No data to save.")

    async def save_data(self):
        """
        Сохранение данных.
        """
        async with self.lock:
            await self._save_file()
            self.cached = False
    
    async def get_data(self, data):
        """
        Возвращает текущие данные класса
        
        Returns:
            any: Данные, записанные в классе
        """
        return self.data

    async def set_data(self, data):
        """
        Записывает в data класса кастомные данные

        Args:
            data (any): Данные для записи в класс
        """
        self.data = data
