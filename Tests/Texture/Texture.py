import os
import unittest

from PIL import Image

from Code.texture_manager import RGBColor, Texture


class TestTexture(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.test_dir = os.path.join(self.base_path, 'test_sprites')
        self.dms_dir = os.path.join(self.test_dir, 'test.dms')
        self.info_yml_path = os.path.join(self.dms_dir, 'info.yml')

        os.makedirs(self.dms_dir, exist_ok=True)

        with open(self.info_yml_path, 'w') as f:
            f.write("""
            Author: Test Author
            License: Test License
            Sprites:
              - name: sprite1
                size: {x: 10, y: 20}
                is_mask: false
                frames: 5
              - name: sprite2
                size: {x: 15, y: 25}
                is_mask: true
                frames: 10
            """)

        for sprite in ['sprite1', 'sprite2']:
            image = Image.new('RGBA', (50, 20), (255, 255, 255, 0))
            image.save(os.path.join(self.dms_dir, f"{sprite}.png"))

        self.texture = Texture(self.dms_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(self.test_dir)

    def test_init(self):
        """Тестирует инициализацию объекта Texture."""
        self.assertEqual(self.texture._path, self.dms_dir)
        self.assertEqual(len(self.texture._allow_state), 2)

    def test_cash_mask(self):
        """Тестирует метод _cash_mask."""
        mask_name = 'sprite1.png'
        color = RGBColor((255, 0, 0, 255))
        self.texture._cash_mask(mask_name, color)
        save_path = os.path.join(self.dms_dir, 'cached_sprite1.png')
        self.assertTrue(os.path.exists(save_path))

    def test_get_image(self):
        """Тестирует метод get_image."""
        img = self.texture.get_image('sprite1')
        self.assertIsInstance(img, Image.Image)

        img = self.texture.get_image('nonexistent')
        self.assertIsNone(img)

    def test_getitem(self):
        """Тестирует метод __getitem__."""
        state_info = self.texture['sprite1']
        self.assertIsNotNone(state_info)
        self.assertEqual(state_info[0], 'sprite1')

        state_info = self.texture['nonexistent']
        self.assertIsNone(state_info)

    def test_create_gif_from_sprite(self):
        """Тестирует метод create_gif_from_sprite."""
        state = 'sprite1'
        fps = 10
        self.texture.create_gif_from_sprite(state, fps=fps)
        output_path = os.path.join(self.dms_dir, f"{state}.gif")
        self.assertTrue(os.path.exists(output_path))

    def test_create_gif_from_sprite_missing_state(self):
        """Тестирует метод create_gif_from_sprite при отсутствии состояния."""
        with self.assertRaises(ValueError):
            self.texture.create_gif_from_sprite('nonexistent')

    def test_create_gif_from_sprite_missing_image(self):
        """Тестирует метод create_gif_from_sprite при отсутствии изображения."""
        os.remove(os.path.join(self.dms_dir, 'sprite2.png'))
        with self.assertRaises(FileNotFoundError):
            self.texture.create_gif_from_sprite('sprite2')


if __name__ == '__main__':
    unittest.main()
