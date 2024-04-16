import hashlib
import logging
import os
import pickle


class FileWork:
    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса FileWork.
        """
        if cls is FileWork:
            raise NotImplementedError("You cannot create an abstract 'FileWork' class. Use inheritance")
        return super().__new__(cls)

    def __init__(self, file_path) -> None:
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
        file_path = file_path.replace('/', os.sep)
        self._path = os.path.join(os.getcwd(), 'Data.DM-Bot', file_path)
        self._data = None
        self._cached = False
        self._file_hash = None

    def create_file(self) -> bool:
        """
        Создание директории и файла, если они не были созданы ранее.
        
        Returns:
            bool: Возвращает True если файл был создан, иначе False
        """
        directory = os.path.dirname(self._path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._path):
            with open(self._path, "wb") as file:
                pickle.dump(None, file)
                return True
        return False

    def _calculate_file_hash(self) -> str:
        """
        Рассчитывает хеш файла.

        Returns:
            str: Хеш файла.
        """
        hasher = hashlib.sha256()
        with open(self._path, 'rb') as file:
            chunk = file.read(8192)
            while chunk:
                hasher.update(chunk)
                chunk = file.read(8192)
        return hasher.hexdigest()

    def _load_file(self) -> bytes:
        """
        Загрузка данных из файла.

        Returns:
            object: Данные файла.
        """
        try:
            with open(self._path, 'rb') as file:
                return file.read()
        except Exception as e:
            logging.error(f"An error occurred in {self._path}: {e}")
            return None

    def load_data(self) -> object:
        """
        Загрузка данных с использованием кэширования и проверки хеша файла.

        Returns:
            object: Загруженные данные файла.
        """
        current_hash = self._calculate_file_hash()
        if not self._cached or self._file_hash != current_hash:
            file_content = self._load_file()
            if file_content is not None:
                self._data = pickle.loads(file_content)
                self._cached = True
                self._file_hash = current_hash
        return self._data

    def _save_file(self) -> None:
        """
        Сохранение данных в файл.
        """
        if self._data is not None:
            with open(self._path, 'wb') as file:
                file.write(pickle.dumps(self._data))

    def save_data(self) -> None:
        """
        Сохранение данных.
        """
        self._save_file()
        self._cached = False
    
    @property
    def data(self) -> object:
        """
        Возвращает текущие данные класса
        
        Returns:
            any: Данные, записанные в классе
        """
        return self._data

    @data.setter
    def data(self, data) -> None:
        """
        Записывает в data класса кастомные данные

        Args:
            data (any): Данные для записи в класс
        """
        self._data = data
