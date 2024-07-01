from PIL import Image, ImageSequence
import yaml
import os
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import hashlib
import pickle


class TextureSystem:
    __slots__ = []
    DEFAULT_FPS: int = 24
    DEFAULT_COLOR: Tuple[int, int, int, int] = (255, 255, 255, 255)
    
    def __init__(self) -> None:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sprites', 'compiled'))
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    @staticmethod
    def _get_hash_list(layers: List[Dict[str, Any]]) -> str:
        serialized_data = pickle.dumps(layers)
        hash_object = hashlib.sha256(serialized_data)
        return hash_object.hexdigest()
    
    @staticmethod
    def _check_and_get_compiled(is_gif: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(path: str, state: str, *args, **kwargs) -> Any:
                color = kwargs.get('color', None)
                image = TextureSystem._get_compiled(path, state, color, is_gif)
                if image:
                    return image
                
                return func(path, state, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def _slice_image(image: Image.Image, frame_width: int, frame_height: int, num_frames: int) -> List[Image.Image]:
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
        TextureSystem._validate_color(color)
        return '_'.join(map(str, color))
    
    @staticmethod
    def _validate_color(color: Tuple[int, int, int, int]) -> None:
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("Invalid RGBA color format for texture. All values must be between 0 и 255")

    @staticmethod
    def get_textures(path: str) -> List[Dict[str, Any]]:
        with open(f"{path}/info.yml", 'r') as file:
            info = yaml.safe_load(file)
        
        return info.get('Sprites', [])

    @staticmethod
    def get_state_info(path: str, state: str) -> Tuple[int, int, int, bool]:
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
    @_check_and_get_compiled(is_gif=False)
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
    @_check_and_get_compiled(is_gif=False)
    def get_image(path: str, state: str) -> Image.Image:
        raise FileNotFoundError(f"Image file for state '{state}' not found in path '{path}'.")

    @staticmethod
    @_check_and_get_compiled(is_gif=True)
    def get_gif_recolor(path: str, state: str, color: Tuple[int, int, int, int] = DEFAULT_COLOR, fps: int = DEFAULT_FPS) -> List[Image.Image]:
        image = TextureSystem.get_image_recolor(path, state, color)
        
        frame_width, frame_height, num_frames, _ = TextureSystem.get_state_info(path, state)
        
        frames = TextureSystem._slice_image(image, frame_width, frame_height, num_frames)
        
        output_path = f"{path}/{state}_compiled_{TextureSystem._get_color_str(color)}.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000//fps, loop=0)
        
        return frames
    
    @staticmethod
    @_check_and_get_compiled(is_gif=True)
    def get_gif(path: str, state: str, fps: int = DEFAULT_FPS) -> List[Image.Image]:
        image = TextureSystem.get_image(path, state)
        frame_width, frame_height, num_frames, _ = TextureSystem.get_state_info(path, state)
        
        frames = TextureSystem._slice_image(image, frame_width, frame_height, num_frames)
        
        output_path = f"{path}/{state}.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000//fps, loop=0)
        
        return frames
        
    @staticmethod
    def merge_layers(layers: List[Dict[str, Any]], fps: int = DEFAULT_FPS) -> Union[Image.Image, List[Image.Image]]:
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
                final_images = [frame.copy() for frame in TextureSystem.get_gif_recolor(first_layer['path'], first_layer['state'], first_layer['color'], fps)]
            else:
                final_images = [frame.copy() for frame in TextureSystem.get_gif(first_layer['path'], first_layer['state'], fps)]
        else:
            if is_mask:
                final_image = TextureSystem.get_image_recolor(first_layer['path'], first_layer['state'], first_layer['color']).copy()
            else:
                final_image = TextureSystem.get_image(first_layer['path'], first_layer['state']).copy()
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
                        if i < len(final_images):
                            final_images[i] = Image.alpha_composite(final_images[i], recolored_frame_expanded)
                        else:
                            final_images.append(recolored_frame_expanded)
                else:
                    normal_frames = TextureSystem.get_gif(layer['path'], layer['state'], fps)
                    for i in range(max_frames):
                        normal_frame_expanded = Image.new("RGBA", (max_width, max_height))
                        frame_to_use = normal_frames[min(i, len(normal_frames) - 1)]  # Используем последний кадр, если i превышает количество кадров
                        normal_frame_expanded.paste(frame_to_use, (0, 0))
                        if i < len(final_images):
                            final_images[i] = Image.alpha_composite(final_images[i], normal_frame_expanded)
                        else:
                            final_images.append(normal_frame_expanded)
            else:
                if is_mask:
                    recolored_image = TextureSystem.get_image_recolor(layer['path'], layer['state'], layer['color'])
                    recolored_image_expanded = Image.new("RGBA", (max_width, max_height))
                    recolored_image_expanded.paste(recolored_image, (0, 0))
                    for i in range(len(final_images)):
                        final_images[i] = Image.alpha_composite(final_images[i], recolored_image_expanded)
                else:
                    normal_image = TextureSystem.get_image(layer['path'], layer['state'])
                    normal_image_expanded = Image.new("RGBA", (max_width, max_height))
                    normal_image_expanded.paste(normal_image, (0, 0))
                    for i in range(len(final_images)):
                        final_images[i] = Image.alpha_composite(final_images[i], normal_image_expanded)
        
        # Создаем новое изображение с максимальными размерами
        if is_gif:
            final_images[0].save(path, save_all=True, append_images=final_images[1:], duration=1000//fps, loop=0)
            return final_images
        
        else:
            final_images[0].save(path)
            return final_images[0]
