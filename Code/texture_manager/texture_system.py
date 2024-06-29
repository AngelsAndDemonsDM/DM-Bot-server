import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

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

    @staticmethod
    def is_mask(path: str, state: str) -> bool:
        """Проверка, является ли текстура маской.

        Args:
            path (str): Путь до текстуры.
            state (str): Стейт текстуры в пути.

        Returns:
            bool: True, если текстура является маской, иначе False.
        """
        texture_states = TextureSystem._get_texture_states(path)
        texture_info = next((sprite for sprite in texture_states if sprite['name'] == state), None)
        
        if texture_info is None:
            raise ValueError(f"State '{state}' not found in info.yml")
        
        return texture_info['is_mask']
    
    def get_texture_and_info(self, path: str, state: str) -> Optional[Tuple[Image.Image, int, int, bool, int]]:
        """
        Метод получения текстуры, координат x и y, является ли маской и количества кадров анимации.

        Args:
            path (str): Путь до текстуры.
            state (str): Стейт текстуры в пути.

        Returns:
            Optional[Tuple[Image.Image, int, int, bool, int]]: изображение, x, y, маска ли, количество кадров анимации.
        """
        try:
            texture_states = self._get_texture_states(path)
            texture_info = next((sprite for sprite in texture_states if sprite['name'] == state), None)
            
            if texture_info is None:
                raise ValueError(f"State '{state}' not found in info.yml")
            
            with Image.open(f"{path}/{texture_info['name']}.png") as image:
                x = texture_info['size']['x']
                y = texture_info['size']['y']
                is_mask = texture_info['is_mask']
                frame_count = texture_info['frames']
            
                return image.copy(), x, y, is_mask, frame_count
        
        except Exception as err:
            logging.error(f"An error occurred while getting texture '{state}' in '{path}': {err}")
        
        return None

    def get_recolor_mask(self, path: str, state: str, color: Tuple[int, int, int, int]) -> Image.Image:
        """Получает или создает перекрашенную маску изображения.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Returns:
            Image.Image: Измененное изображение.
        """
        TextureSystem._validate_color(color)
        if not TextureSystem.is_mask(path, state):
            raise ValueError(f"Texture {state} in {path} is not a mask")
        
        return self._get_recolor_mask(path, state, color)
        
    def _get_recolor_mask(self, path: str, state: str, color: Tuple[int, int, int, int]) -> Image.Image:
        """Получает или создает перекрашенную маску изображения.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Returns:
            Image.Image: Измененное изображение.
        """
        image_path = f"{path}/{state}_compiled_{self._get_color_str(color)}.png"
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                return img.copy()

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
            image.save(image_path)
            return image

    def _validate_gif_params(self, path: str, state: str) -> None:
        """Проверка валидности параметров для создания GIF-анимации.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.

        Raises:
            ValueError: Если состояние не найдено или количество кадров равно нулю.
        """
        texture_info = next((sprite for sprite in self._get_texture_states(path) if sprite['name'] == state), None)
        if texture_info is None:
            raise ValueError(f"State '{state}' not found in info.yml")
        if texture_info['frames'] == 0:
            raise ValueError(f"No frames specified for state '{state}' in {path}")

    def get_gif(self, path: str, state: str, fps: Optional[int] = 24) -> Image.Image:
        """Получает или создает GIF-анимацию из спрайтового листа.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.

        Returns:
            Image.Image: GIF-анимация.
        """
        self._validate_gif_params(path, state)
        gif_path = os.path.join(path, f"{state}_compiled.gif")
        return self._get_gif(path, state, gif_path, fps)

    def _get_gif(self, path: str, state: str, gif_path: str, fps: int) -> Image.Image:
        """Получает или создает GIF-анимацию из спрайтового листа.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            gif_path (str): Путь для сохранения GIF-анимации.
            fps (int): Частота кадров в секунду для GIF-анимации.

        Returns:
            Image.Image: GIF-анимация.
        """
        if os.path.exists(gif_path):
            with Image.open(gif_path) as img:
                return img.copy()

        texture_info = next((sprite for sprite in self._get_texture_states(path) if sprite['name'] == state), None)
        frame_width = texture_info['size']['x']
        frame_height = texture_info['size']['y']
        num_frames = texture_info['frames']
        
        with Image.open(f"{path}/{texture_info['name']}.png") as image:
            frames = self._slice_image(image, frame_width, frame_height, num_frames)
            duration = int(1000 / fps)
            self._create_gif(frames, gif_path, duration)

        with Image.open(gif_path) as gif_image:
            return gif_image.copy()

    def get_recolor_gif(self, path: str, state: str, color: Tuple[int, int, int, int], fps: Optional[int] = 24) -> Image.Image:
        """Получает или создает перекрашенную GIF-анимацию из спрайтового листа.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            color (Tuple[int, int, int, int]): Цвет для перекраски маски.
            fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.

        Returns:
            Image.Image: Перекрашенная GIF-анимация.
        """
        self._validate_gif_params(path, state)
        self._validate_color(color)
        gif_path = os.path.join(path, f"{state}_compiled_{self._get_color_str(color)}.gif")
        return self._get_recolor_gif(path, state, color, gif_path, fps)

    def _get_recolor_gif(self, path: str, state: str, color: Tuple[int, int, int, int], gif_path: str, fps: int) -> Image.Image:
        """Получает или создает перекрашенную GIF-анимацию из спрайтового листа.

        Args:
            path (str): Путь до папки с изображениями.
            state (str): Имя состояния изображения.
            color (Tuple[int, int, int, int]): Цвет для перекраски маски.
            gif_path (str): Путь для сохранения GIF-анимации.
            fps (int): Частота кадров в секунду для GIF-анимации.

        Returns:
            Image.Image: Перекрашенная GIF-анимация.
        """
        if os.path.exists(gif_path):
            with Image.open(gif_path) as img:
                return img.copy()

        texture_info = next((sprite for sprite in self._get_texture_states(path) if sprite['name'] == state), None)
        frame_width = texture_info['size']['x']
        frame_height = texture_info['size']['y']
        num_frames = texture_info['frames']
        
        image = self._get_recolor_mask(path, state, color)
        frames = self._slice_image(image, frame_width, frame_height, num_frames)
        duration = int(1000 / fps)
        self._create_gif(frames, gif_path, duration)

        with Image.open(gif_path) as gif_image:
            return gif_image.copy()

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
        image_width, image_height = image.size

        for i in range(num_frames):
            row = (i * frame_width) // image_width
            col = (i * frame_width) % image_width
            box = (col, row * frame_height, col + frame_width, row * frame_height + frame_height)
            frame = image.crop(box)
            frames.append(frame)
        
        return frames

    @staticmethod
    def _create_gif(frames: List[Image.Image], gif_path: str, duration: int) -> None:
        """Создает GIF-анимацию из списка кадров.

        Args:
            frames (List[Image.Image]): Список кадров.
            gif_path (str): Путь для сохранения GIF-анимации.
            duration (int): Продолжительность каждого кадра в миллисекундах.
        """
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=duration, loop=0)

    def merge_layers(self, layers: List[Dict[str, Any]], fps: Optional[int] = 24) -> Union[Image.Image, List[Image.Image]]:
        """
        Метод для сложения всех слоев и возврата результата.

        Args:
            layers (List[Dict[str, Any]]): Список словарей, каждый из которых содержит 'path', 'state' и 'color' (необязательно).
            fps (Optional[int]): Частота кадров в секунду для GIF-анимации. По умолчанию 24 fps.

        Returns:
            Union[Image.Image, List[Image.Image]]: Результирующее изображение или список изображений для анимации.
        """
        base_images = []
        common_size = (0, 0)

        for layer in layers:
            path = layer['path']
            state = layer['state']
            color = layer.get('color')

            if color:
                base_image = self.get_compiled_texture(path, state, color, fps)
            else:
                base_image = self.get_compiled_texture(path, state, (255, 255, 255, 255), fps)

            if isinstance(base_image, list):
                base_images.append(base_image)
                common_size = (max(common_size[0], base_image[0].size[0]), max(common_size[1], base_image[0].size[1]))
            else:
                base_images.append([base_image])
                common_size = (max(common_size[0], base_image.size[0]), max(common_size[1], base_image.size[1]))

        for images in base_images:
            for i in range(len(images)):
                if images[i].size != common_size:
                    images[i] = images[i].resize(common_size, Image.ANTIALIAS)

        for images in base_images:
            for img in images:
                print(f"Image size: {img.size}")

        if any(isinstance(images, list) for images in base_images):
            max_frames = max(len(images) for images in base_images)
            merged_frames = []

            for frame_index in range(max_frames):
                merged_frame = Image.new('RGBA', common_size)
                
                for images in base_images:
                    if frame_index < len(images):
                        merged_frame = Image.alpha_composite(merged_frame, images[frame_index])
                    else:
                        merged_frame = Image.alpha_composite(merged_frame, images[-1])
                
                merged_frames.append(merged_frame)

            return merged_frames
        
        else:
            merged_image = Image.new('RGBA', common_size)

            for images in base_images:
                merged_image = Image.alpha_composite(merged_image, images[0])

            return merged_image

    def get_compiled_texture(self, path: str, state: str, color: Tuple[int, int, int, int], fps: int) -> Union[Image.Image, List[Image.Image]]:
        img, x, y, is_mask, frames = self.get_texture_and_info(path, state)
        
        if is_mask:
            if frames > 1:
                return self.get_recolor_gif(path, state, color, fps)
            else:
                return self.get_recolor_mask(path, state, color)
        
        else:
            if frames > 1:
                return self.get_gif(path, state, fps)
            else:
                return img
