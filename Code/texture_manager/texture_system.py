import os
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import yaml
from PIL import Image, ImageSequence


class TextureSystem:
    __slots__ = []
    DEFAULT_FPS: int = 24
    DEFAULT_COLOR: Tuple[int, int, int, int] = (255, 255, 255, 255)
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def _check_and_get_compiled(func: Callable) -> Callable:
        """Декоратор для проверки наличия скомпилированного изображения или GIF-файла.

        Args:
            func (Callable): Функция, к которой применяется декоратор.

        Returns:
            Callable: Обернутая функция, которая сначала проверяет наличие скомпилированного файла. Если файл найден, он возвращается. Если нет, выполняется оригинальная функция.
        """
        @wraps(func)
        def wrapper(path: str, state: str, *args, **kwargs) -> Any:
            color = kwargs.get('color', None)
            is_gif = kwargs.get('is_gif', False)
            image = TextureSystem._get_compiled(path, state, color, is_gif)
            if image:
                return image
            
            return func(path, state, *args, **kwargs)
        
        return wrapper
    
    @staticmethod
    def _slice_image(image: Image.Image, frame_width: int, frame_height: int, num_frames: int) -> List[Image.Image]:
        """Нарезает изображение на кадры заданного размера.

        Args:
            image (Image.Image): Исходное изображение, которое нужно нарезать.
            frame_width (int): Ширина каждого кадра.
            frame_height (int): Высота каждого кадра.
            num_frames (int): Общее количество кадров, которые нужно вырезать из изображения.

        Returns:
            List[Image.Image]: Список вырезанных кадров в виде объектов Image.
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
    def _get_color_str(color: Tuple[int, int, int, int]) -> str:
        """_summary_

        Args:
            color (Tuple[int, int, int, int]): _description_

        Returns:
            str: _description_
        """
        TextureSystem._validate_color(color)
        return '_'.join(map(str, color))
    
    @staticmethod
    def _validate_color(color: Tuple[int, int, int, int]) -> None:
        """_summary_

        Args:
            color (Tuple[int, int, int, int]): _description_

        Raises:
            ValueError: _description_
        """
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("Invalid RGBA color format for texture. All values must be between 0 и 255")

    @staticmethod
    def get_textures(path: str) -> List[Dict[str, Any]]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[Dict[str, Any]]: _description_
        """
        with open(f"{path}/info.yml", 'r') as file:
            info = yaml.safe_load(file)
        
        return info.get('Sprites', [])

    @staticmethod
    def _get_compiled(path: str, state: str, color: Optional[Tuple[int, int, int, int]] = None, is_gif: bool = False) -> Union[Image.Image, List[Image.Image], None]:
        """Получает скомпилированное изображение или GIF.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            color (Optional[Tuple[int, int, int, int]]): Цвет для перекрашивания. По умолчанию None.
            is_gif (bool): Флаг, указывающий, что нужно вернуть GIF. По умолчанию False.

        Returns:
            Union[Image.Image, List[Image.Image], None]: Изображение или список кадров GIF, или None, если файл не найден.
        """
        image_path: str = f"{path}/{state}"
        if color:
            image_path += f"_compiled_{TextureSystem._get_color_str(color)}"
        
        image_path += ".gif" if is_gif else ".png"
        
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                if is_gif:
                    return [frame.convert("RGBA").copy() for frame in ImageSequence.Iterator(img)]
                else:
                    return img.convert("RGBA").copy()
        
        else:
            return None
    
    @staticmethod
    @_check_and_get_compiled
    def get_image_recolor(path: str, state: str, color: Tuple[int, int, int, int] = DEFAULT_COLOR) -> Image.Image:
        with Image.open(f"{path}/{state}.png") as image:
            image = image.convert("RGBA")
            new_colored_image = [
                (
                    int(pixel[0] * color[0] / 255),
                    int(pixel[0] * color[1] / 255),
                    int(pixel[0] * color[2] / 255),
                    pixel[3]
                ) if pixel[3] != 0 else pixel
                for pixel in image.getdata()
            ]

            image.putdata(new_colored_image)
            image.save(f"{path}/{state}_compiled_{TextureSystem._get_color_str(color)}.png")
            return image
    
    @staticmethod
    @_check_and_get_compiled
    def get_image(path: str, state: str) -> Image.Image:
        raise FileNotFoundError(f"Image file for state '{state}' not found in path '{path}'.") # lol
    
    @staticmethod
    @_check_and_get_compiled
    def get_gif_recolor(path: str, state: str, fps: int = DEFAULT_FPS, color: Tuple[int, int, int, int] = DEFAULT_COLOR):
        pass

    
    @staticmethod
    @_check_and_get_compiled
    def get_gif(path: str, state: str, fps: int = DEFAULT_FPS):
        pass
