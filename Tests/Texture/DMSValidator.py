import shutil
import unittest
from pathlib import Path

from Code.systems.texture_validator import (DMSValidator, InvalidSpriteError,
                                            SpriteValidationError)


class TestDMSValidator(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).resolve().parent.parent.parent
        self.test_dir = self.base_path / 'test_sprites'
        self.dms_dir = self.test_dir / 'test.dms'
        self.info_yml_path = self.dms_dir / 'info.yml'

        self.dms_dir.mkdir(parents=True, exist_ok=True)
        
        with self.info_yml_path.open('w') as f:
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
            (self.dms_dir / f"{sprite}.png").touch()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_validate_dms(self):
        self.assertTrue(DMSValidator.validate_dms(self.test_dir, 'test.dms'))

    def test_validate_all_dms(self):
        self.assertTrue(DMSValidator.validate_all_dms(self.test_dir))

    def test_missing_info_yml(self):
        self.info_yml_path.unlink()
        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("info.yml not found" in str(context.exception))

    def test_invalid_sprite_format(self):
        with self.info_yml_path.open('w') as f:
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
        (self.dms_dir / 'sprite1.png').unlink()
        with self.assertRaises(InvalidSpriteError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("Missing files" in str(context.exception))

    def test_check_forbidden_files(self):
        forbidden_file_path = self.dms_dir / '_compiled_file.txt'
        with forbidden_file_path.open('w') as f:
            f.write("This is a forbidden file.")

        with self.assertRaises(InvalidSpriteError) as context:
            DMSValidator.validate_dms(self.test_dir, 'test.dms')
        
        self.assertTrue("Forbidden file or directory found" in str(context.exception))

    def test_sprite_name_contains_forbidden_pattern(self):
        with self.info_yml_path.open('w') as f:
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
        non_existent_dir = self.test_dir / 'non_existent.dms'
        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'non_existent.dms')
        
        self.assertTrue("DMS does not exist" in str(context.exception))

    def test_not_a_directory(self):
        not_a_directory_path = self.test_dir / 'not_a_directory.dms'
        not_a_directory_path.write_text("This is not a directory.")

        with self.assertRaises(SpriteValidationError) as context:
            DMSValidator.validate_dms(self.test_dir, 'not_a_directory.dms')
        
        self.assertTrue("DMS is not a directory" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
