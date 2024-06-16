import os
import unittest
from typing import Dict, List, Union

import yaml


class SpriteValidationError(Exception):
    """Базовый класс для исключений, связанных с валидацией спрайтов."""
    def __init__(self, message: str, path: str):
        super().__init__(message)
        self.message = message
        self.path = path

class InvalidSpriteError(SpriteValidationError):
    """Исключение для случаев, когда файл info.yml отсутствует или содержит неверные данные.

    Args:
        message (str): Сообщение об ошибке.
        path (str): Путь к файлу.
        missing_files (List[str]): Список недостающих файлов.
        missing_field (str): Отсутствующее поле.
    """
    def __init__(self, message: str, path: str, missing_files: List[str] = None, missing_field: str = None):
        super().__init__(message, path)
        self.missing_files = missing_files
        self.missing_field = missing_field

# Функция для проверки наличия info.yml в папке
def check_info_yml_exists(folder_path: str) -> bool:
    """Проверяет наличие файла info.yml в указанной папке.

    Args:
        folder_path (str): Путь к папке.

    Raises:
        InvalidSpriteError: Исключение, если файл info.yml не найден.

    Returns:
        bool: True, если файл найден.
    """
    info_yml_path = os.path.join(folder_path, 'info.yml')
    
    if not os.path.isfile(info_yml_path):
        raise InvalidSpriteError("info.yml not found", info_yml_path)
    
    return True

# Функция для проверки содержания info.yml
def validate_info_yml(folder_path: str) -> Dict[str, Union[str, List[str]]]:
    """Проверяет содержание файла info.yml.

    Args:
        folder_path (str): Путь к папке.

    Raises:
        InvalidSpriteError: Исключение, если отсутствует обязательное поле или если поле 'Sprites' не является списком строк.

    Returns:
        Dict[str, Union[str, List[str]]]: Содержимое файла info.yml.
    """
    info_yml_path = os.path.join(folder_path, 'info.yml')
    with open(info_yml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    required_fields = ['Author', 'License', 'Sprites']
    for field in required_fields:
        if field not in data:
            raise InvalidSpriteError(f"Missing required field: {field}", info_yml_path, missing_field=field)
    
    # Дополнительные проверки для полей
    if not isinstance(data['Sprites'], list) or not all(isinstance(item, str) for item in data['Sprites']):
        raise InvalidSpriteError(f"Field 'Sprites' must be a list of strings", info_yml_path)
    
    return data

# Функция для проверки наличия файлов, указанных в info.yml
def check_files_exist(folder_path: str, files_list: List[str]) -> bool:
    """Проверяет наличие файлов, указанных в info.yml.

    Args:
        folder_path (str): Путь к папке.
        files_list (List[str]): Список файлов.

    Raises:
        InvalidSpriteError: Исключение, если файл из списка не найден.

    Returns:
        bool: True, если все файлы найдены.
    """
    missing_files = []
    for file_name in files_list:
        file_path = os.path.join(folder_path, f"{file_name}.png")
        if not os.path.isfile(file_path):
            missing_files.append(f"{file_name}.png")
    
    if missing_files:
        raise InvalidSpriteError("Missing files", folder_path, missing_files=missing_files)
    
    return True

# Основная функция для проверки папки
def validate_folder(folder_path: str) -> bool:
    """Проверяет папку на наличие файла info.yml и соответствующих файлов спрайтов.

    Args:
        folder_path (str): Путь к папке.

    Returns:
        bool: True, если папка валидна, иначе исключение.
    """
    check_info_yml_exists(folder_path)
    info_data = validate_info_yml(folder_path)
    check_files_exist(folder_path, info_data['Sprites'])
    
    return True

# Функция для поиска всех папок с расширением .dms в корневой директории и их проверки
def validate_all_dms_folders(root_path: str) -> Dict[str, bool]:
    """Ищет все папки с расширением .dms в корневой директории и проверяет их.

    Args:
        root_path (str): Путь к корневой директории.

    Returns:
        Dict[str, bool]: Словарь с результатами проверки для каждой папки.
    """
    results = {}
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        
        if os.path.isdir(item_path) and item.endswith('.dms'):
            is_valid = validate_folder(item_path)
            results[item] = is_valid
            
    return results

class TestSpriteFolders(unittest.TestCase):
    def setUp(self):
        self.root_path = 'Sprites'

    def test_validate_all_dms_folders(self):
        results = validate_all_dms_folders(self.root_path)
        
        for folder, is_valid in results.items():
            with self.subTest(folder=folder):
                self.assertTrue(is_valid, msg=f"Validation failed for {folder}")

if __name__ == '__main__':
    unittest.main()
