from pathlib import Path
from typing import Dict, List, Union

import yaml


class SpriteValidationError(Exception):
    """Базовый класс для исключений, связанных с валидацией спрайтов.

    Этот класс расширяет стандартный класс исключений и добавляет дополнительную информацию о пути к файлу, где произошла ошибка.

    Args:
        message (str): Сообщение об ошибке, описывающее, что пошло не так.
        path (Union[str, Path]): Путь к файлу, в котором произошла ошибка.
    """
    def __init__(self, message: str, path: Union[str, Path]):
        super().__init__(message)
        self.message = message
        self.path = Path(path)

    def __str__(self):
        return f"{self.message} (Path: {self.path})"


class InvalidSpriteError(SpriteValidationError):
    """Исключение для случаев, когда файл info.yml отсутствует или содержит неверные данные.

    Этот класс расширяет SpriteValidationError и добавляет информацию о недостающих файлах или полях.

    Args:
        message (str): Сообщение об ошибке, описывающее, что пошло не так.
        path (Union[str, Path]): Путь к файлу, в котором произошла ошибка.
        missing_files (List[str], optional): Список недостающих файлов. По умолчанию None.
        missing_field (str, optional): Отсутствующее поле в файле info.yml. По умолчанию None.
    """
    def __init__(self, message: str, path: Union[str, Path], missing_files: List[str] = None, missing_field: str = None):
        super().__init__(message, path)
        self.missing_files = missing_files
        self.missing_field = missing_field

    def __str__(self):
        details = []
        if self.missing_files:
            details.append(f"Missing files: {', '.join(self.missing_files)}")
        if self.missing_field:
            details.append(f"Missing field: {self.missing_field}")
        details_str = "; ".join(details) if details else "No additional details"
        return f"{self.message} (Path: {self.path}; Details: {details_str})"


class DMSValidator:
    __slots__ = []
    INFO_REQUIRED_FIELDS: List[str] = ['Author', 'License', 'Sprites']
    SPRITE_REQUIRED_FIELDS: List[str] = ['name', 'size', 'is_mask', 'frames']

    COMPILED_PATTERNS = ['_compiled', '_compiled_']

    @staticmethod
    def _raise_dms_file(path: Union[str, Path]) -> None:
        """Проверяет существование директории DMS и является ли она директорией.

        Args:
            path (Union[str, Path]): Путь к директории.

        Raises:
            SpriteValidationError: Если DMS не существует или не является директорией.
        """
        path = Path(path)
        if not path.exists():
            raise SpriteValidationError("DMS does not exist", path)

        if not path.is_dir():
            raise SpriteValidationError("DMS is not a directory", path)

    @staticmethod
    def _load_dms_info(path: Union[str, Path]) -> Dict:
        """Загружает информацию из файла info.yml.

        Args:
            path (Union[str, Path]): Путь к директории DMS.

        Raises:
            SpriteValidationError: Если файл info.yml не найден или отсутствуют обязательные поля.

        Returns:
            Dict: Содержимое info.yml.
        """
        path = Path(path)
        yml_path = path / "info.yml"
        if not yml_path.is_file():
            raise SpriteValidationError("info.yml not found", path)

        with yml_path.open('r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)

        for field in DMSValidator.INFO_REQUIRED_FIELDS:
            if field not in info_yml:
                raise InvalidSpriteError(f"Missing required field", yml_path, field)

        return info_yml

    @staticmethod
    def _validate_sprites_format(sprites: List[Dict], info_yml_path: Path) -> None:
        """Проверяет формат спрайтов в info.yml.

        Args:
            sprites (List[Dict]): Список спрайтов.
            info_yml_path (Path): Путь к info.yml.

        Raises:
            InvalidSpriteError: Если формат спрайтов некорректен или отсутствуют обязательные поля.
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

            # Проверка на имя спрайта
            sprite_name = sprite['name']
            for pattern in DMSValidator.COMPILED_PATTERNS:
                if pattern in sprite_name:
                    raise InvalidSpriteError(f"Sprite name '{sprite_name}' contains forbidden pattern: {pattern}", info_yml_path)

    @staticmethod
    def _check_files_exist(folder_path: Union[str, Path], sprites: List[Dict[str, Union[str, Dict[str, int], bool]]]) -> None:
        """Проверяет наличие файлов спрайтов в директории.

        Args:
            folder_path (Union[str, Path]): Путь к директории.
            sprites (List[Dict[str, Union[str, Dict[str, int], bool]]]): Список спрайтов.

        Raises:
            InvalidSpriteError: Если один или несколько файлов спрайтов отсутствуют.
        """
        folder_path = Path(folder_path)
        missing_files = []

        for sprite in sprites:
            file_name = sprite['name']
            file_path = folder_path / f"{file_name}.png"
            if not file_path.is_file():
                missing_files.append(f"{file_name}.png")

        if missing_files:
            raise InvalidSpriteError("Missing files", folder_path, missing_files=missing_files)

    @staticmethod
    def _check_forbidden_files(folder_path: Union[str, Path]) -> None:
        """Проверяет наличие запрещенных файлов или директорий.

        Args:
            folder_path (Union[str, Path]): Путь к директории.

        Raises:
            InvalidSpriteError: Если найдены запрещенные файлы или директории.
        """
        folder_path = Path(folder_path)
        for path in folder_path.rglob("*"):
            for pattern in DMSValidator.COMPILED_PATTERNS:
                if pattern in path.name:
                    raise InvalidSpriteError(f"Forbidden file or directory found: {path.name}", folder_path)

    @staticmethod
    def validate_dms_dirrect(dms_path: Union[str, Path]) -> bool:
        """Валидирует директорию DMS.

        Args:
            dms_path (Union[str, Path]): Путь к директории DMS.

        Returns:
            bool: True, если валидация прошла успешно.

        Raises:
            SpriteValidationError: Если директория не существует, не является директорией или некорректна структура.
        """
        dms_path = Path(dms_path)
        DMSValidator._raise_dms_file(dms_path)

        info_yml = DMSValidator._load_dms_info(dms_path)
        DMSValidator._validate_sprites_format(info_yml['Sprites'], dms_path)
        DMSValidator._check_files_exist(dms_path, info_yml['Sprites'])
        DMSValidator._check_forbidden_files(dms_path)

        return True

    @staticmethod
    def validate_dms(base_path: Union[str, Path], dms_path: Union[str, Path]) -> bool:
        """Валидирует конкретную директорию DMS относительно базового пути.

        Args:
            base_path (Union[str, Path]): Базовый путь к директории с текстурами.
            dms_path (Union[str, Path]): Путь к директории DMS относительно базового пути.

        Returns:
            bool: True, если валидация прошла успешно.

        Raises:
            SpriteValidationError: Если директория не существует, не является директорией или некорректна структура.
        """
        base_path = Path(base_path)
        dms_path = base_path / dms_path

        DMSValidator._raise_dms_file(dms_path)

        info_yml = DMSValidator._load_dms_info(dms_path)
        DMSValidator._validate_sprites_format(info_yml['Sprites'], dms_path)
        DMSValidator._check_files_exist(dms_path, info_yml['Sprites'])
        DMSValidator._check_forbidden_files(dms_path)

        return True

    @staticmethod
    def validate_all_dms(base_path: Union[str, Path]) -> bool:
        """Валидирует все директории DMS в базовой директории.

        Args:
            base_path (Union[str, Path]): Базовый путь к директории с текстурами.

        Returns:
            bool: True, если валидация всех директорий прошла успешно.

        Raises:
            SpriteValidationError: Если хотя бы одна директория некорректна.
        """
        base_path = Path(base_path)
        for item in base_path.iterdir():
            if item.is_dir() and item.suffix == '.dms':
                DMSValidator.validate_dms(base_path, item)

        return True
