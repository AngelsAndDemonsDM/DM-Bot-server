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
        DMSValidator().validate_dms_dirrect(path_to_dms)
        self._path: str = path_to_dms

        self._allow_state: List[Tuple[str, int, bool, Tuple[int, int]]] = []
        self._get_states()

    def _cash_mask(self, mask: str, color: RGBColor) -> None:
        """Создает и сохраняет изображение маски с заданным цветом.

        Args:
            mask (str): Имя файла маски.
            color (RGBColor): Цвет для перекраски маски.
        """
        image = TextureManager.recolor_mask(os.path.join(self._path, mask), color)
        save_path = os.path.join(self._path, f"cached_{mask}")
        image.save(save_path, format='PNG')

    def _get_states(self) -> None:
        """Загружает состояния спрайтов из файла info.yml и сохраняет их в атрибут _allow_state.
        """
        yml_path = os.path.join(self._path, "info.yml")
        
        with open(yml_path, 'r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)
        
        for item in info_yml['Sprites']:
            self._allow_state.append((item['name'], item['is_mask'], item['frames'], (item['size']['x'], item['size']['y'])))

    def get_image(self, state: str) -> Optional[Image.Image]:
        """Возвращает изображение для заданного состояния.

        Args:
            state (str): Название состояния.

        Returns:
            Optional[Image.Image]: Изображение состояния или None, если изображение не найдено.
        """
        for item in self._allow_state:
            if item[0] == state:
                image_path = os.path.join(self._path, f"{state}.png")
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    return image
        
        return None

    def __getitem__(self, key: str) -> Optional[Tuple[str, int, bool, Tuple[int, int]]]:
        """Возвращает информацию о состоянии по его имени.

        Args:
            key (str): Название состояния.

        Returns:
            Optional[Tuple[str, int, bool, Tuple[int, int]]]: Кортеж с информацией о состоянии или None, если состояние не найдено.
        """
        for item in self._allow_state:
            if item[0] == key:
                return item
        
        return None

    def create_gif_from_sprite(self, state: str, fps: int = 60) -> None:
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

        name, is_mask, frames, (frame_width, frame_height) = state_info
        sprite_image = self.get_image(state)
        
        sprite_width, sprite_height = sprite_image.size
        gif_frames = []
        frame_duration = int(1000 / fps)

        for y in range(0, sprite_height, frame_height):
            for x in range(0, sprite_width, frame_width):
                if len(gif_frames) >= frames:
                    break
                box = (x, y, x + frame_width, y + frame_height)
                frame = sprite_image.crop(box)
                gif_frames.append(frame)

        output_path = os.path.join(self._path, f"{state}.gif")
        gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:], optimize=False, duration=frame_duration, loop=0)
