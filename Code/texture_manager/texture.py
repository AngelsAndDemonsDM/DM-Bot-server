import os
from typing import List, Optional, Tuple

import yaml
from PIL import Image
from texture_manager.color import RGBColor
from texture_manager.texture_manager import TextureManager
from texture_manager.texture_validator import DMSValidator


class Texture:
    __slots__ = ['_path', '_allow_state']

    def __init__(self, path_to_dms: str) -> None:
        """Инициализация объекта Texture. Проверяет корректность директории и загружает состояния из файла info.yml.

        Args:
            path_to_dms (str): Путь к директории с данными DMS.
        """
        DMSValidator.validate_dms_dirrect(path_to_dms)
        self._path: str = path_to_dms
        self._allow_state: List[Tuple[str, int, bool, Tuple[int, int]]] = []
        self._load_states()

    def _load_states(self) -> None:
        """Загружает состояния спрайтов из файла info.yml и сохраняет их в атрибут _allow_state."""
        yml_path = os.path.join(self._path, "info.yml")
        with open(yml_path, 'r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)

        self._allow_state = [
            (item['name'], item['is_mask'], item['frames'], (item['size']['x'], item['size']['y']))
            for item in info_yml['Sprites']
        ]

    def _cache_mask_image(self, mask: str, color: RGBColor) -> None:
        """Создает и сохраняет изображение маски с заданным цветом.

        Args:
            mask (str): Имя файла маски.
            color (RGBColor): Цвет для перекраски маски.
        """
        image = TextureManager.recolor_mask(os.path.join(self._path, mask), color)
        save_path = os.path.join(self._path, f"cached_{mask}_{color.get_hex()}.png")
        image.save(save_path, format='PNG')

    def _generate_gif_frames(self, sprite_image: Image.Image, state_info: Tuple[str, int, bool, Tuple[int, int]], fps: int, color: Optional[RGBColor] = None) -> Tuple[List[Image.Image], int]:
        """Генерирует кадры для GIF-анимации из изображения спрайта.

        Args:
            sprite_image (Image.Image): Изображение спрайта.
            state_info (Tuple[str, int, bool, Tuple[int, int]]): Информация о состоянии.
            fps (int): Частота кадров в секунду.
            color (Optional[RGBColor], optional): Цвет для перекраски маски. По умолчанию None.

        Returns:
            Tuple[List[Image.Image], int]: Список кадров GIF и длительность одного кадра в миллисекундах.
        """
        name, is_mask, frames, (frame_width, frame_height) = state_info
        sprite_width, sprite_height = sprite_image.size
        gif_frames = []
        frame_duration = int(1000 / fps)

        for y in range(0, sprite_height, frame_height):
            for x in range(0, sprite_width, frame_width):
                if len(gif_frames) >= frames:
                    return gif_frames, frame_duration
                box = (x, y, x + frame_width, y + frame_height)
                frame = sprite_image.crop(box)
                if color:
                    frame = TextureManager.recolor_mask(frame, color)
                gif_frames.append(frame)

        return gif_frames, frame_duration

    def __getitem__(self, key: str) -> Optional[Tuple[str, int, bool, Tuple[int, int]]]:
        """Возвращает информацию о состоянии по его имени.

        Args:
            key (str): Название состояния.

        Returns:
            Optional[Tuple[str, int, bool, Tuple[int, int]]]: Кортеж с информацией о состоянии или None, если состояние не найдено.
        """
        return next((item for item in self._allow_state if item[0] == key), None)

    def get_image(self, state: str) -> Optional[Image.Image]:
        """Возвращает изображение для заданного состояния.

        Args:
            state (str): Название состояния.

        Returns:
            Optional[Image.Image]: Изображение состояния или None, если изображение не найдено.
        """
        image_path = os.path.join(self._path, f"{state}.png")
        return Image.open(image_path) if os.path.exists(image_path) else None

    def create_gif(self, state: str, fps: int = 60) -> None:
        """Создает и сохраняет GIF-анимацию для заданного состояния.

        Args:
            state (str): Название состояния.
            fps (int, optional): Частота кадров в секунду. По умолчанию 60.

        Raises:
            ValueError: Если состояние не найдено в _allow_state.
            FileNotFoundError: Если изображение для состояния не найдено.
        """
        state_info = self[state]
        if state_info is None:
            raise ValueError(f"State '{state}' not found in Texture.")

        sprite_image = self.get_image(state)
        if sprite_image is None:
            raise FileNotFoundError(f"Image for state '{state}' not found.")

        gif_frames, frame_duration = self._generate_gif_frames(sprite_image, state_info, fps)
        output_path = os.path.join(self._path, f"{state}.gif")
        gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:], optimize=False, duration=frame_duration, loop=0)

    def get_cached_mask(self, state: str, color: RGBColor) -> Image.Image:
        """Находит закешированный спрайт маски если есть, если нет - кеширует и возвращает.

        Args:
            state (str): Название состояния.
            color (RGBColor): Цвет для перекраски маски.

        Returns:
            Image.Image: Изображение маски.
        """
        cache_file = os.path.join(self._path, f"cached_{state}_{color.get_hex()}.png")
        if not os.path.exists(cache_file):
            self._cache_mask_image(state, color)
        return Image.open(cache_file)

    def get_cached_gif(self, state: str, fps: int = 60) -> Image.Image:
        """Находит закешированный спрайт гиф если есть, если нет - кеширует и возвращает.

        Args:
            state (str): Название состояния.
            fps (int, optional): Частота кадров в секунду. По умолчанию 60.

        Returns:
            Image.Image: GIF изображение.
        """
        gif_file = os.path.join(self._path, f"{state}.gif")
        if not os.path.exists(gif_file):
            self.create_gif(state, fps)
        return Image.open(gif_file)

    def create_colored_gif(self, state: str, color: RGBColor, fps: int = 60) -> Image.Image:
        """Создает GIF из покрашенной маски.

        Args:
            state (str): Название состояния.
            color (RGBColor): Цвет для перекраски маски.
            fps (int, optional): Частота кадров в секунду. По умолчанию 60.

        Returns:
            Image.Image: GIF изображение.
        """
        state_info = self[state]
        if state_info is None:
            raise ValueError(f"State '{state}' not found in Texture.")

        sprite_image = self.get_image(state)
        if sprite_image is None:
            raise FileNotFoundError(f"Image for state '{state}' not found.")

        gif_frames, frame_duration = self._generate_gif_frames(sprite_image, state_info, fps, color)
        output_path = os.path.join(self._path, f"cached_{state}_{color.get_hex()}.gif")
        gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:], optimize=False, duration=frame_duration, loop=0)

        return Image.open(output_path)
