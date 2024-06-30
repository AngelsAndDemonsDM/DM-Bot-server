import os
from typing import Any, Dict, List, Tuple

import yaml
from PIL import Image
from texture_manager.texture_validator import DMSValidator


class TextureSystem:
    __slots__ = ['_sprite_path']
    
    def __init__(self, path: str) -> None:
        """Класс для работы со спрайтами. Используйте уже объявленный из Code.main_impt

        Args:
            path (str): Путь до папки со всеми спрайтами
        """
        DMSValidator(path).validate_all_dms()
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self._sprite_path = os.path.join(base_path, path.replace('/', os.sep))

    @staticmethod
    def _get_color_str(color: Tuple[int, int, int, int]) -> str:
        """Преобразует цвет в строку с разделителями.

        Args:
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Returns:
            str: Цвет в формате строки.
        """
        return '_'.join(map(str, color))
    
    @staticmethod
    def _validate_color(color: Tuple[int, int, int, int]) -> None:
        """Проверка валидности цвета в формате RGBA.

        Args:
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Raises:
            ValueError: Если значения цвета не находятся в диапазоне от 0 до 255.
        """
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("Invalid RGBA color format for texture. All values must be between 0 и 255")

    @staticmethod
    def _slice_image(image: Image.Image, frame_width: int, frame_height: int, num_frames: int) -> List[Image.Image]:
        """Нарезает изображение на кадры.

        Args:
            image (Image.Image): Исходное изображение.
            frame_width (int): Ширина кадра.
            frame_height (int): Высота кадра.
            num_frames (int): Количество кадров.

        Returns:
            List[Image.Image]: Список кадров.
        """
        frames = []
        image_width, _ = image.size

        for i in range(num_frames):
            row = (i * frame_width) // image_width
            col = (i * frame_width) % image_width
            box = (col, row * frame_height, col + frame_width, row * frame_height + frame_height)
            frame = image.crop(box)
            frame = frame.convert("RGBA")
            frames.append(frame)
        
        return frames

    @staticmethod
    def _get_texture_states(path: str) -> List[Dict[str, Any]]:
        """Получение списка состояний текстур из файла info.yml.

        Args:
            path (str): Путь до папки с файлом info.yml.

        Returns:
            List[Dict[str, Any]]: Список словарей с состояниями текстур.
        """
        with open(f"{path}/info.yml", 'r') as file:
            info = yaml.safe_load(file)
        
        return info.get('Sprites', [])
