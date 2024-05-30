from PIL import Image


def add_color_to_base_image(base_image_path, color):
    base_image = Image.open(base_image_path).convert("RGBA")
    new_data = [
        (
            int(pixel[0] * color[0] / 255),
            int(pixel[0] * color[1] / 255),
            int(pixel[0] * color[2] / 255),
            pixel[3]
        ) if pixel[3] != 0 else pixel
        for pixel in base_image.getdata()
    ]
    base_image.putdata(new_data)
    return base_image

def overlay_images(base_image, overlay_image_path):
    overlay_image = Image.open(overlay_image_path).convert("RGBA").resize(base_image.size)
    return Image.alpha_composite(base_image, overlay_image)

base_image_path = "123_c.png"
overlay_image_path = "123.png"
color = (255, 0, 0, 255)  # Пример цвета в RGBA

# Добавляем цвет к базовому изображению
colored_base_image = add_color_to_base_image(base_image_path, color)

# Накладываем оверлей на базовое изображение
final_image = overlay_images(colored_base_image, overlay_image_path)

new_image_path = "final_combined_image.png"
final_image.save(new_image_path)
