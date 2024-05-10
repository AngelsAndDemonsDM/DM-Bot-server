import hashlib
import os
import pickle


class BinFileData:
    """
    Класс для работы с бинарными файлами.

    Attributes:
        _path (str): Полный путь к файлу.
        _data (object): Данные файла.
        _cached (bool): Флаг, указывающий, кэшированы ли данные.
        _file_hash (str): Хеш файла.
    """
    def __init__(self, file_path: str) -> None:
        """
        Инициализация объекта BinFileData.

        Args:
            file_path (str): Путь к файлу.

        Examples:
            Создание экземпляра класса BinFileData для работы с файлом "example_data.bin"
            ```py
            file_data = BinFileData("example_data")
            ```
        """
        file_path = file_path + ".bin"
        file_path = file_path.replace('/', os.sep)
        self._path = os.path.join(os.getcwd(), 'Data.DM-Bot', file_path)
        self._create_file()
        self._data = None
        self._cached = False
        self._file_hash = None

    def _create_file(self) -> bool:
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

        Raises:
            FileNotFoundError: Если файл не найден.
        """
        if not os.path.exists(self._path):
            raise FileNotFoundError(f"Файл {self._path} не найден")
    
        with open(self._path, 'rb') as file:
            return file.read()

    def load_data(self) -> object:
        """
        Загрузка данных с использованием кэширования и проверки хеша файла.

        Returns:
            object: Загруженные данные файла.

        Raises:
            FileNotFoundError: Если файл не найден.

        Examples:
            Загрузка данных из файла "example_data.bin"
            ```py
            loaded_data = file_data.load_data()
            print("Загруженные данные из файла:", loaded_data)
            ```
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

        Examples:
            Сохранение данных в файл "example_data.bin"
            ```py
            file_data.save_data()
            ```
        """
        self._save_file()
        self._cached = False
    
    @property
    def data(self) -> object:
        """
        Возвращает или записывает данные
        
        Returns:
            any: Данные, записанные в классе

        Examples:
            Получение данных из объекта класса
            ```py
            file_data = BinFileData("example_data")
            file_data.data = 123
            file_data.save_data()
            file_data.data = 124
            file_data.load_data()
            print("Данные из объекта класса:", file_data.data)
            ```
            print выведет `Данные из объекта класса: 123`
        """
        return self._data

    @data.setter
    def data(self, data) -> None:
        self._data = data
