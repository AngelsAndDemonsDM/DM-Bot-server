import os
from typing import Dict, List, Union

import yaml
from texture_manager.texture_errors import (InvalidSpriteError,
                                            SpriteValidationError)


class DMSValidator:
    __slots__ = ["_sprite_path"]
    INFO_REQUIRED_FIELDS: List[str] = ['Author', 'License', 'Sprites']
    SPRITE_REQUIRED_FIELDS: List[str] = ['name', 'size', 'is_mask', 'frames']
    
    def __init__(self, path: str) -> None:
        """
        Инициализирует DMSValidator с указанным путем.

        Args:
            path (str): Относительный путь к папке.

        Raises:
            FileNotFoundError: Если директория не существует.
        """
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        full_path = os.path.join(base_path, path.replace('/', os.sep))
        
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            raise FileNotFoundError(f"Directory '{full_path}' does not exist.")
        
        self._sprite_path: str = full_path

    @staticmethod
    def _raise_dms_file(path: str) -> None:
        """
        Проверяет, существует ли папка и является ли она директорией.

        Args:
            path (str): Путь к проверяемой папке.

        Raises:
            SpriteValidationError: Если папка не существует или не является директорией.
        """
        if not os.path.exists(path):
            raise SpriteValidationError("DMS does not exist", path)
        
        if not os.path.isdir(path):
            raise SpriteValidationError("DMS is not a directory", path)
    
    @staticmethod
    def _load_dms_info(path: str) -> Dict:
        """
        Загружает и проверяет файл info.yml.

        Args:
            path (str): Путь к папке.

        Raises:
            SpriteValidationError: Если файл info.yml не найден или отсутствует обязательное поле.

        Returns:
            Dict: Содержимое файла info.yml.
        """
        yml_path = os.path.join(path, "info.yml")
        if not os.path.isfile(yml_path):
            raise SpriteValidationError("info.yml not found", path)
        
        with open(yml_path, 'r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)
        
        for field in DMSValidator.INFO_REQUIRED_FIELDS:
            if field not in info_yml:
                raise SpriteValidationError(f"Missing required field: {field}", yml_path)
        
        return info_yml
    
    @staticmethod
    def _validate_sprites_format(sprites: List[Dict], info_yml_path: str) -> None:
        """
        Проверяет формат поля 'Sprites'.

        Args:
            sprites (List[Dict]): Список спрайтов для проверки.
            info_yml_path (str): Путь к файлу info.yml.

        Raises:
            InvalidSpriteError: Если формат спрайтов неверен.
        """
        if not isinstance(sprites, list) or not all(isinstance(item, dict) for item in sprites):
            raise InvalidSpriteError(f"Field 'Sprites' must be a list of dictionaries", info_yml_path)
        
        for sprite in sprites:
            for field in DMSValidator.SPRITE_REQUIRED_FIELDS:
                if field not in sprite:
                    raise InvalidSpriteError(f"Missing required field in sprite: {field}", info_yml_path)

            if not isinstance(sprite['size'], dict) or not all(k in sprite['size'] for k in ['x', 'y']):
                raise InvalidSpriteError("Each sprite 'size' must be a dictionary with 'x' and 'y' fields", info_yml_path)
            
            frames = sprite['frames']
            if not isinstance(frames, int) or frames < 0:
                raise InvalidSpriteError(f"Frame count must be a non-negative integer", info_yml_path)
    
    @staticmethod
    def _check_files_exist(folder_path: str, sprites: List[Dict[str, Union[str, Dict[str, int], bool]]]) -> None:
        """
        Проверяет наличие файлов, указанных в info.yml.

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

    def validate_dms(self, dms_path: str) -> bool:
        """
        Проверяет папку DMS.

        Args:
            dms_path (str): Путь к папке DMS относительно корневой папки.

        Returns:
            bool: Результат проверки папки.
        """
        dms_path = os.path.join(self._sprite_path, dms_path.replace('/', os.sep))
        
        DMSValidator._raise_dms_file(dms_path)
        
        info_yml = DMSValidator._load_dms_info(dms_path)
        DMSValidator._validate_sprites_format(info_yml['Sprites'], dms_path)
        DMSValidator._check_files_exist(dms_path, info_yml['Sprites'])
        
        return True

    def validate_all_dms(self) -> bool:
        """
        Проверяет все папки с расширением .dms в корневой директории.

        Returns:
            bool: Результат проверки всех папок.
        """
        for item in os.listdir(self._sprite_path):
            item_path = os.path.join(self._sprite_path, item)
            
            if os.path.isdir(item_path) and item.endswith('.dms'):
                self.validate_dms(item_path)
        
        return True
