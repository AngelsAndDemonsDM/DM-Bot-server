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
            Author: "themanyfaceddemon"
            License: "NONE. IT IS TEST"
            Sprites:
              - name: "sprite1"
                size: {x: 10, y: 20}
                is_mask: false
                frames: 5
              - name: "sprite2"
                size: {x: 15, y: 25}
                is_mask: true
                frames: 10
            """)

        for sprite in ['sprite1', 'sprite2']:
            open(os.path.join(self.dms_dir, f"{sprite}.png"), 'a').close()

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        
        os.rmdir(self.test_dir)

    def test_validate_dms(self):
        self.assertTrue(DMSValidator.validate_dms(self.test_dir, 'test.dms'))

    def test_validate_all_dms(self):
        self.assertTrue(DMSValidator.validate_all_dms(self.test_dir))

    def test_missing_info_yml(self):
        os.remove(self.info_yml_path)
        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("info.yml not found" in str(context.exception))

    def test_invalid_sprite_format(self):
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
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("Each sprite 'size' must be a dictionary with 'x' and 'y' fields" in str(context.exception))

    def test_missing_sprite_file(self):
        os.remove(os.path.join(self.dms_dir, 'sprite1.png'))
        with self.assertRaises(InvalidSpriteError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("Missing files" in str(context.exception))

    def test_check_forbidden_files(self):
        forbidden_file_path = os.path.join(self.dms_dir, '_compiled_file.txt')
        with open(forbidden_file_path, 'w') as f:
            f.write("This is a forbidden file.")

        with self.assertRaises(InvalidSpriteError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("Forbidden file or directory found" in str(context.exception))

    def test_sprite_name_contains_forbidden_pattern(self):
        with open(self.info_yml_path, 'w') as f:
            f.write("""
            Author: "themanyfaceddemon"
            License: "NONE. IT IS TEST"
            Sprites:
              - name: "_compiled_sprite1"
                size: {x: 10, y: 20}
                is_mask: false
                frames: 5
              - name: "sprite2"
                size: {x: 15, y: 25}
                is_mask: true
                frames: 10
            """)

        with self.assertRaises(InvalidSpriteError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("contains forbidden pattern" in str(context.exception))

    def test_non_existent_directory(self):
        non_existent_dir = os.path.join(self.test_dir, 'non_existent.dms')
        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'non_existent.dms')
        
        self.assertTrue("DMS does not exist" in str(context.exception))

    def test_not_a_directory(self):
        not_a_directory_path = os.path.join(self.test_dir, 'not_a_directory.dms')
        with open(not_a_directory_path, 'w') as f:
            f.write("This is not a directory.")

        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'not_a_directory.dms')
        
        self.assertTrue("DMS is not a directory" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
