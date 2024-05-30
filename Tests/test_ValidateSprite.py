import os
import yaml
import unittest

class SpriteValidationError(Exception):
    pass

class MissingSpriteFileError(SpriteValidationError):
    pass

class InvalidSpriteInfoYmlError(SpriteValidationError):
    pass

# Функция для проверки наличия info.yml в папке
def check_info_yml_exists(folder_path):
    info_yml_path = os.path.join(folder_path, 'info.yml')
    if not os.path.isfile(info_yml_path):
        raise MissingSpriteFileError(f"info.yml not found in {folder_path}")
    return True

# Функция для проверки содержания info.yml
def validate_info_yml(folder_path):
    info_yml_path = os.path.join(folder_path, 'info.yml')
    with open(info_yml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    required_fields = ['Author', 'License', 'Sprites']
    for field in required_fields:
        if field not in data:
            raise InvalidSpriteInfoYmlError(f"Missing required field: {field} in {info_yml_path}")
    
    # Дополнительные проверки для полей
    if not isinstance(data['Sprites'], list) or not all(isinstance(item, str) for item in data['Sprites']):
        raise InvalidSpriteInfoYmlError(f"Field 'Sprites' must be a list of strings in {info_yml_path}")
    
    return data

# Функция для проверки наличия файлов, указанных в info.yml
def check_files_exist(folder_path, files_list):
    missing_files = []
    for file_name in files_list:
        file_path = os.path.join(folder_path, file_name)
        if not os.path.isfile(file_path):
            missing_files.append(file_name)
    
    if missing_files:
        raise MissingSpriteFileError(f"Missing files in {folder_path}: {', '.join(missing_files)}")
    return True

# Основная функция для проверки папки
def validate_folder(folder_path):
    try:
        check_info_yml_exists(folder_path)
        info_data = validate_info_yml(folder_path)
        check_files_exist(folder_path, info_data['Sprites'])
        return True, "Folder is valid"
    except InvalidSpriteInfoYmlError as err:
        return False, str(err)

# Функция для поиска всех папок с расширением .dms в корневой директории и их проверки
def validate_all_dms_folders(root_path):
    results = {}
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path) and item.endswith('.dms'):
            is_valid, message = validate_folder(item_path)
            results[item] = (is_valid, message)
    return results

class TestSpriteFolders(unittest.TestCase):
    def setUp(self):
        self.root_path = '/Sprites'

    def test_validate_all_dms_folders(self):
        results = validate_all_dms_folders(self.root_path)
        for folder, (is_valid, message) in results.items():
            print(f"{folder}: {message}")
            self.assertTrue(is_valid, msg=f"Validation failed for {folder}: {message}")

if __name__ == '__main__':
    unittest.main()
