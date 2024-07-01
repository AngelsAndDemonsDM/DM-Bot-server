import unittest

from Code.texture_manager import (DMSValidator, InvalidSpriteError,
                                  SpriteValidationError)


class TestTextureFolders(unittest.TestCase):
    def setUp(self):
        self.dms_validator = DMSValidator('Sprites')

    def test_validate_all_dms_folders(self):
        try:
            result = self.dms_validator.validate_all_dms()
            self.assertTrue(result)
        
        except (SpriteValidationError, InvalidSpriteError) as e:
            error_message = f"validate_all_dms raised an exception: {e.message}, Path: {e.path}"
            if isinstance(e, InvalidSpriteError):
                if e.missing_files:
                    error_message += f", Missing Files: {e.missing_files}"
                if e.missing_field:
                    error_message += f", Missing Field: {e.missing_field}"
            
            self.fail(error_message)

if __name__ == '__main__':
    unittest.main()
