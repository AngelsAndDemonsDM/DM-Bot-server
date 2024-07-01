import hashlib
import os
import pickle
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import yaml
from PIL import Image, ImageSequence


class TextureSystem:
    """Класс TextureSystem отвечает за управление текстурами, включая их загрузку, изменение цвета, и объединение слоев в одно изображение или GIF.
    """
    __slots__ = []
    DEFAULT_FPS: int = 24
    DEFAULT_COLOR: Tuple[int, int, int, int] = (255, 255, 255, 255)
    
    def __init__(self) -> None:
        """Инициализирует систему текстур и создает базовую директорию для компилированных спрайтов, если она не существует.
        """
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sprites', 'compiled'))
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    @staticmethod
    def _get_hash_list(layers: List[Dict[str, Any]]) -> str:
        """Возвращает хеш списка слоев для идентификации уникальных комбинаций.

        Args:
            layers (List[Dict[str, Any]]): Список слоев.

        Returns:
            str: Хеш в виде строки.
        """
        serialized_data = pickle.dumps(layers)
        hash_object = hashlib.sha256(serialized_data)
        return hash_object.hexdigest()
    
    @staticmethod
    def _slice_image(image: Image.Image, frame_width: int, frame_height: int, num_frames: int) -> List[Image.Image]:
        """Разрезает изображение на кадры заданного размера.

        Args:
            image (Image.Image): Изображение для разрезания.
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
    def _get_color_str(color: Tuple[int, int, int, int]) -> str:
        """Возвращает строковое представление цвета.

        Args:
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Returns:
            str: Строковое представление цвета.
        """
        TextureSystem._validate_color(color)
        return '_'.join(map(str, color))
    
    @staticmethod
    def _validate_color(color: Tuple[int, int, int, int]) -> None:
        """Проверяет, что цвет в формате RGBA имеет корректные значения.

        Args:
            color (Tuple[int, int, int, int]): Цвет в формате RGBA.

        Raises:
            ValueError: Если значения цвета находятся вне диапазона 0-255.
        """
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("Invalid RGBA color format for texture. All values must be between 0 и 255")

    @staticmethod
    def get_textures(path: str) -> List[Dict[str, Any]]:
        """Загружает текстуры из указанного пути.

        Args:
            path (str): Путь к файлу с текстурами.

        Returns:
            List[Dict[str, Any]]: Список текстур.
        """
        with open(f"{path}/info.yml", 'r') as file:
            info = yaml.safe_load(file)
        
        return info.get('Sprites', [])

    @staticmethod
    def get_state_info(path: str, state: str) -> Tuple[int, int, int, bool]:
        """Получает информацию о состоянии текстуры из файла.

        Args:
            path (str): Путь к файлу с текстурами.
            state (str): Имя состояния.

        Raises:
            ValueError: Если информация о состоянии не найдена.

        Returns:
            Tuple[int, int, int, bool]: Ширина кадра, высота кадра, количество кадров и флаг маски.
        """
        with open(f"{path}/info.yml", 'r') as file:
            info = yaml.safe_load(file)
        
        info = info.get('Sprites', [])

        sprite_info = next((sprite for sprite in info if sprite['name'] == state), None)
        if not sprite_info:
            raise ValueError(f"No sprite info found for state '{state}' in path '{path}'")
        
        frame_width = sprite_info['size']['x']
        frame_height = sprite_info['size']['y']
        num_frames = sprite_info['frames']
        is_mask = sprite_info['is_mask']

        return frame_width, frame_height, num_frames, is_mask
    
    @staticmethod
    def _get_compiled(path: str, state: str, color: Optional[Tuple[int, int, int, int]] = None, is_gif: bool = False) -> Union[Image.Image, List[Image.Image], None]:
        """Проверяет наличие компилированного изображения или GIF.

        Args:
            path (str): Путь к файлу.
            state (str): Имя состояния.
            color (Optional[Tuple[int, int, int, int]], optional): Цвет в формате RGBA. По умолчанию None.
            is_gif (bool, optional): Указывает, является ли изображение GIF. По умолчанию False.

        Returns:
            Union[Image.Image, List[Image.Image], None]: Изображение или список кадров, если существует, иначе None.
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
    def get_image_recolor(path: str, state: str, color: Tuple[int, int, int, int] = DEFAULT_COLOR) -> Image.Image:
        """Возвращает перекрашенное изображение указанного состояния.

        Args:
            path (str): Путь к файлу.
            state (str): Имя состояния.
            color (Tuple[int, int, int, int], optional): Цвет в формате RGBA. По умолчанию DEFAULT_COLOR.

        Returns:
            Image.Image: Перекрашенное изображение.
        """
        image = TextureSystem._get_compiled(path, state, color, False)
        if image:
            return image
        
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
    def get_image(path: str, state: str) -> Image.Image:
        """Возвращает изображение указанного состояния.

        Args:
            path (str): Путь к файлу.
            state (str): Имя состояния.

        Raises:
            FileNotFoundError: Если файл изображения не найден.

        Returns:
            Image.Image: Изображение состояния.
        """
        image = TextureSystem._get_compiled(path, state, None, False)
        if image:
            return image
        
        raise FileNotFoundError(f"Image file for state '{state}' not found in path '{path}'.")

    @staticmethod
    def get_gif_recolor(path: str, state: str, color: Tuple[int, int, int, int] = DEFAULT_COLOR, fps: int = DEFAULT_FPS) -> List[Image.Image]:
        """Возвращает перекрашенный GIF указанного состояния.

        Args:
            path (str): Путь к файлу.
            state (str): Имя состояния.
            color (Tuple[int, int, int, int], optional): Цвет в формате RGBA. По умолчанию DEFAULT_COLOR.
            fps (int, optional): Частота кадров. По умолчанию DEFAULT_FPS.

        Returns:
            List[Image.Image]: Список кадров перекрашенного GIF.
        """
        image = TextureSystem._get_compiled(path, state, color, True)
        if image:
            return image
        
        image = TextureSystem.get_image_recolor(path, state, color)
        
        frame_width, frame_height, num_frames, _ = TextureSystem.get_state_info(path, state)
        
        frames = TextureSystem._slice_image(image, frame_width, frame_height, num_frames)
        
        output_path = f"{path}/{state}_compiled_{TextureSystem._get_color_str(color)}.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000//fps, loop=0)
        
        return frames
    
    @staticmethod
    def get_gif(path: str, state: str, fps: int = DEFAULT_FPS) -> List[Image.Image]:
        """Возвращает GIF указанного состояния.

        Args:
            path (str): Путь к файлу.
            state (str): Имя состояния.
            fps (int, optional): Частота кадров. По умолчанию DEFAULT_FPS.

        Returns:
            List[Image.Image]: Список кадров GIF.
        """
        image = TextureSystem._get_compiled(path, state, None, True)
        if image:
            return image
        
        image = TextureSystem.get_image(path, state)
        frame_width, frame_height, num_frames, _ = TextureSystem.get_state_info(path, state)
        
        frames = TextureSystem._slice_image(image, frame_width, frame_height, num_frames)
        
        output_path = f"{path}/{state}.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000//fps, loop=0)
        
        return frames

    @staticmethod
    def merge_images(background: Image.Image, overlay: Image.Image, position: Tuple[int, int] = (0, 0)) -> Image.Image:
        """Накладывает изображение overlay на изображение background с учетом прозрачности.
        
        Args:
            background (Image.Image): Фоновое изображение.
            overlay (Image.Image): Изображение, которое накладывается.
            position (Tuple[int, int]): Позиция (x, y), куда будет накладываться overlay. По умолчанию (0, 0).

        Returns:
            Image.Image: Объединенное изображение.
        """
        # Создаем копию фонового изображения
        merged_image = background.copy()
        
        # Извлекаем альфа-канал из накладываемого изображения
        overlay_alpha = overlay.split()[3]
        
        # Накладываем изображение с учетом прозрачности
        merged_image.paste(overlay, position, overlay_alpha)
        
        return merged_image

    @staticmethod
    def merge_layers(layers: List[Dict[str, Any]], fps: int = DEFAULT_FPS) -> Union[Image.Image, List[Image.Image]]:
        """Объединяет слои в одно изображение или GIF.

        Args:
            layers (List[Dict[str, Any]]): Список слоев.
            fps (int, optional): Частота кадров для GIF. По умолчанию DEFAULT_FPS.

        Returns:
            Union[Image.Image, List[Image.Image]]: Объединенное изображение или список кадров GIF.
        """
        hash_layers = TextureSystem._get_hash_list(layers)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sprites', 'compiled', hash_layers))
        
        is_gif: bool = False
        max_width: int = 0
        max_height: int = 0
        max_frames: int = 0
        
        for layer in layers:
            frame_width, frame_height, num_frames, _ = TextureSystem.get_state_info(layer['path'], layer['state'])
            max_width = max(max_width, frame_width)
            max_height = max(max_height, frame_height)
            max_frames = max(max_frames, num_frames)
            if num_frames > 1:
                is_gif = True
        
        path += ".gif" if is_gif else ".png"
        
        if os.path.exists(path):
            with Image.open(path) as img:
                if is_gif:
                    return [frame.convert("RGBA").copy() for frame in ImageSequence.Iterator(img)]
                else:
                    return img.convert("RGBA").copy()

        # Закончили проверку и поняли, что нам надо работать. Первоначальная обработка первого слоя
        final_images: List[Image.Image] = []
        first_layer = layers[0]
        _, _, _, is_mask = TextureSystem.get_state_info(first_layer['path'], first_layer['state'])

        if is_gif:
            if is_mask:
                final_images = [frame.convert("RGBA") for frame in TextureSystem.get_gif_recolor(first_layer['path'], first_layer['state'], first_layer['color'], fps)]
            else:
                final_images = [frame.convert("RGBA") for frame in TextureSystem.get_gif(first_layer['path'], first_layer['state'], fps)]
        else:
            if is_mask:
                final_image = TextureSystem.get_image_recolor(first_layer['path'], first_layer['state'], first_layer['color']).convert("RGBA")
            else:
                final_image = TextureSystem.get_image(first_layer['path'], first_layer['state']).convert("RGBA")
            
            final_images.append(final_image)

        # Обработка оставшихся слоев
        for layer in layers[1:]:
            _, _, _, is_mask = TextureSystem.get_state_info(layer['path'], layer['state'])

            if is_gif:
                if is_mask:
                    recolored_frames = TextureSystem.get_gif_recolor(layer['path'], layer['state'], layer['color'], fps)
                    for i in range(max_frames):
                        recolored_frame_expanded = Image.new("RGBA", (max_width, max_height))
                        frame_to_use = recolored_frames[min(i, len(recolored_frames) - 1)]  # Используем последний кадр, если i превышает количество кадров
                        recolored_frame_expanded.paste(frame_to_use, (0, 0))
                        recolored_frame_expanded = recolored_frame_expanded.convert("RGBA")
                        if i < len(final_images):
                            final_images[i] = TextureSystem.merge_images(final_images[i], recolored_frame_expanded)
                        else:
                            final_images.append(recolored_frame_expanded)
                else:
                    normal_frames = TextureSystem.get_gif(layer['path'], layer['state'], fps)
                    for i in range(max_frames):
                        normal_frame_expanded = Image.new("RGBA", (max_width, max_height))
                        frame_to_use = normal_frames[min(i, len(normal_frames) - 1)]  # Используем последний кадр, если i превышает количество кадров
                        normal_frame_expanded.paste(frame_to_use, (0, 0))
                        normal_frame_expanded = normal_frame_expanded.convert("RGBA")
                        if i < len(final_images):
                            final_images[i] = TextureSystem.merge_images(final_images[i], normal_frame_expanded)
                        else:
                            final_images.append(normal_frame_expanded)
            else:
                if is_mask:
                    recolored_image = TextureSystem.get_image_recolor(layer['path'], layer['state'], layer['color'])
                    recolored_image_expanded = Image.new("RGBA", (max_width, max_height))
                    recolored_image_expanded.paste(recolored_image, (0, 0))
                    recolored_image_expanded = recolored_image_expanded.convert("RGBA")
                    for i in range(len(final_images)):
                        final_images[i] = TextureSystem.merge_images(final_images[i], recolored_image_expanded)
                else:
                    normal_image = TextureSystem.get_image(layer['path'], layer['state'])
                    normal_image_expanded = Image.new("RGBA", (max_width, max_height))
                    normal_image_expanded.paste(normal_image, (0, 0))
                    normal_image_expanded = normal_image_expanded.convert("RGBA")
                    for i in range(len(final_images)):
                        final_images[i] = TextureSystem.merge_images(final_images[i], normal_image_expanded)
        
        # Создаем новое изображение с максимальными размерами
        if is_gif:
            final_images[0].save(path, save_all=True, append_images=final_images[1:], duration=1000//fps, loop=0)
            return final_images.copy()
        
        else:
            final_images[0].save(path)
            return final_images[0].copy()
