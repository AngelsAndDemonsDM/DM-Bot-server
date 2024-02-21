import os
import pickle

class FileWork:
    def __init__(self, path):
        path = os.path.dirname(path)
        self.path = os.path.join(os.getcwd(), '..', 'data', path)
        self.data = None
        self.cached = False  # Флаг, указывающий, были ли данные кэшированы
        self.file_hash = None  # Хеш файла

    def __new__(cls, *args, **kwargs):
        if cls is FileWork:
            raise TypeError("You cannot create an abstract 'FileWork' class. Use inheritanse")
        return super().__new__(cls)
    
    def create_file(self):
        """
        Создание директории и фала если оно не было создано уже
        
        Args:
            None
        
        Returns:
            None
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    

    def _calculate_file_hash(self):
        """
        Рассчитывает хеш файла
        
        Args:
            None
        
        Returns:
            str: Хеш файла
        """
        hasher = hashlib.sha256()
        with open(self.path, 'rb') as file:
            while chunk := file.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _load_file(self):
        """
        Загрузка данных с файла
            
        Args:
            None
            
        Returns:
            data (DataFiles): Загруженный файл данных
        """
        try:
            with open(self.path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"An error occurred in {self.path}: {e}")
            return None

    def load_data(self):
        """
        Загрузка данных с использованием кэширования и проверки хеша файла
        
        Args:
            None
        
        Returns:
            data (DataFiles): Загруженный файл данных
        """
        current_hash = self._calculate_file_hash()
        if not self.cached or self.file_hash != current_hash:
            self.data = self._load_file()
            self.cached = True
            self.file_hash = current_hash
        return self.data

    def _save_file(self):
        """
        Сохранение данных на файл
        
        Args:
            None
        
        Returns:
            None
        """
        if self.data is not None:
            with open(self.path, 'wb') as file:
                pickle.dump(self.data, file)
        else:
            print("No data to save.")

    def save_data(self):
        """
        Сохранение данных
        
        Args:
            None
        
        Returns:
            None
        """
        self._save_file()
        self.cached = False

import os
import pickle
import hashlib
