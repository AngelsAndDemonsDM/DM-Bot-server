import math
from PIL import Image, ImageDraw

def place_icons_around_circle(image, num_icons, icon_path, output_size, circle_radius):
    # Загрузка иконки
    icon = Image.open(icon_path)
    
    # Создание нового изображения
    new_image = Image.new("RGBA", output_size, (255, 255, 255, 0))
    
    # Расчет параметров окружности
    circle_center = (output_size[0] // 2, output_size[1] // 2)
    
    # Расчет угла между иконками
    angle_step = 360 / num_icons
    
    # Размещение иконок вдоль окружности
    for i in range(num_icons):
        angle_deg = angle_step * i
        angle_rad = math.radians(angle_deg)
        
        # Вычисление позиции для каждой иконки
        icon_x = circle_center[0] + int(circle_radius * math.cos(angle_rad)) - icon.size[0] // 2
        icon_y = circle_center[1] + int(circle_radius * math.sin(angle_rad)) - icon.size[1] // 2
        
        # Вычисление угла для поворота иконки
        rotation_angle = 90 - angle_deg
        
        # Поворот иконки
        rotated_icon = icon.rotate(rotation_angle, expand=True)
        
        # Добавление повернутой иконки на изображение
        new_image.paste(rotated_icon, (icon_x, icon_y), rotated_icon)
    
    # Сохранение изображения
    new_image_path = "icons_around_circle.png"
    new_image.save(new_image_path)
    
    print(f"Создано новое изображение: {new_image_path}")

# Параметры
num_icons = 8  # Количество иконок вокруг окружности
icon_path = "your_icon_16x16.png"  # Путь к вашей иконке
output_size = (200, 200)  # Размер нового изображения
circle_radius = 80  # Радиус окружности

# Вызов функции
place_icons_around_circle(None, num_icons, icon_path, output_size, circle_radius)
