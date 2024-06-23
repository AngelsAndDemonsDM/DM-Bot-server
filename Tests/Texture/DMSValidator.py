import os
import unittest

from Code.texture_manager import (DMSValidator, InvalidSpriteError,
                                  SpriteValidationError)


class TestDMSValidator(unittest.TestCase):
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
            open(os.path.join(self.dms_dir, f"{sprite}.png"), 'a').close()

        self.validator = DMSValidator('test_sprites')

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        
        os.rmdir(self.test_dir)

    def test_validate_dms(self):
        """Тестирует метод validate_dms."""
        self.assertTrue(self.validator.validate_dms('test.dms'))

    def test_validate_all_dms(self):
        """Тестирует метод validate_all_dms."""
        self.assertTrue(self.validator.validate_all_dms())

    def test_missing_info_yml(self):
        """Тестирует метод validate_dms при отсутствии файла info.yml."""
        os.remove(self.info_yml_path)
        with self.assertRaises(SpriteValidationError) as context:
            self.validator.validate_dms('test.dms')
        
        self.assertTrue("info.yml not found" in str(context.exception))

    def test_invalid_sprite_format(self):
        """Тестирует метод validate_dms при неверном формате спрайтов."""
        with open(self.info_yml_path, 'w') as f:
            f.write("""
            Author: Test Author
            License: Test License
            Sprites:
              - name: sprite1
                size: {x: 10}
                is_mask: false
                frames: 5
            """)
        
        with self.assertRaises(InvalidSpriteError) as context:
            self.validator.validate_dms('test.dms')
        
        self.assertTrue("Each sprite 'size' must be a dictionary with 'x' and 'y' fields" in str(context.exception))

    def test_missing_sprite_file(self):
        """Тестирует метод validate_dms при отсутствии файлов спрайтов."""
        os.remove(os.path.join(self.dms_dir, 'sprite1.png'))
        with self.assertRaises(InvalidSpriteError) as context:
            self.validator.validate_dms('test.dms')
        
        self.assertTrue("Missing files" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
