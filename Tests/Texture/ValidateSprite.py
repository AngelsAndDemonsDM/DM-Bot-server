import os
import unittest
from typing import Dict, List, Union

import yaml

from Code.texture_manager import InvalidSpriteError, SpriteValidationError


def get_info_yml_path(folder_path: str) -> str:
    """Возвращает путь к файлу info.yml в указанной папке.

    Args:
        folder_path (str): Путь к папке.

    Returns:
        str: Путь к файлу info.yml.
    """
    return os.path.join(folder_path, 'info.yml')

def read_info_yml(info_yml_path: str) -> Dict:
    """Читает и возвращает содержимое файла info.yml.

    Args:
        info_yml_path (str): Путь к файлу info.yml.

    Raises:
        InvalidSpriteError: Если файл info.yml не найден.

    Returns:
        Dict: Содержимое файла info.yml.
    """
    if not os.path.isfile(info_yml_path):
        raise InvalidSpriteError("info.yml not found", info_yml_path)
    
    with open(info_yml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    return data

def validate_required_fields(data: Dict, required_fields: List[str], info_yml_path: str) -> None:
    """Проверяет наличие обязательных полей в данных.

    Args:
        data (Dict): Данные для проверки.
        required_fields (List[str]): Список обязательных полей.
        info_yml_path (str): Путь к файлу info.yml.

    Raises:
        InvalidSpriteError: Если отсутствует обязательное поле.
    """
    for field in required_fields:
        if field not in data:
            raise InvalidSpriteError(f"Missing required field: {field}", info_yml_path, missing_field=field)

def validate_sprites_format(sprites: List[Dict], info_yml_path: str) -> None:
    """Проверяет формат поля 'Sprites'.

    Args:
        sprites (List[Dict]): Список спрайтов для проверки.
        info_yml_path (str): Путь к файлу info.yml.

    Raises:
        InvalidSpriteError: Если формат спрайтов неверен.
    """
    if not isinstance(sprites, list) or not all(isinstance(item, dict) for item in sprites):
        raise InvalidSpriteError(f"Field 'Sprites' must be a list of dictionaries", info_yml_path)
    
    for sprite in sprites:
        if not all(k in sprite for k in ['name', 'size', 'is_mask', 'frames']):
            raise InvalidSpriteError("Each sprite must have 'name', 'size', 'is_mask', and 'frames' fields", info_yml_path)
        
        if not isinstance(sprite['size'], dict) or not all(k in sprite['size'] for k in ['x', 'y']):
            raise InvalidSpriteError("Each sprite 'size' must be a dictionary with 'x' and 'y' fields", info_yml_path)
        
        frames = sprite['frames']
        if not isinstance(frames, int) or frames < 0:
            raise InvalidSpriteError(f"Frame count must be a non-negative integer", info_yml_path)

def check_files_exist(folder_path: str, sprites: List[Dict[str, Union[str, Dict[str, int], bool]]]) -> None:
    """Проверяет наличие файлов, указанных в info.yml.

    Args:
        folder_path (str): Путь к папке.
        sprites (List[Dict[str, Union[str, Dict[str, int], bool]]]): Список спрайтов.

    Raises:
        InvalidSpriteError: Если файл из списка не найден.
    """
    missing_files = []
    for sprite in sprites:
        file_name = sprite['name']
        file_path = os.path.join(folder_path, f"{file_name}.png")
        if not os.path.isfile(file_path):
            missing_files.append(f"{file_name}.png")
    
    if missing_files:
        raise InvalidSpriteError("Missing files", folder_path, missing_files=missing_files)

def validate_folder(folder_path: str) -> None:
    """Проверяет папку на наличие файла info.yml и соответствующих файлов спрайтов.

    Args:
        folder_path (str): Путь к папке.

    Raises:
        InvalidSpriteError: Если файл info.yml не найден или содержит неверные данные.
    """
    info_yml_path = get_info_yml_path(folder_path)
    data = read_info_yml(info_yml_path)
    validate_required_fields(data, ['Author', 'License', 'Sprites'], info_yml_path)
    validate_sprites_format(data['Sprites'], info_yml_path)
    check_files_exist(folder_path, data['Sprites'])

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
            try:
                validate_folder(item_path)
                results[item] = True
            
            except InvalidSpriteError:
                results[item] = False
    
    return results

class TestSpriteFolders(unittest.TestCase):
    def setUp(self):
        self.root_path = 'Sprites'

    def test_validate_all_dms_folders(self):
        """Тестирует функцию validate_all_dms_folders на корневой директории."""
        results = validate_all_dms_folders(self.root_path)
        
        for folder, is_valid in results.items():
            with self.subTest(folder=folder):
                self.assertTrue(is_valid, msg=f"Validation failed for {folder}")

if __name__ == '__main__':
    unittest.main()
