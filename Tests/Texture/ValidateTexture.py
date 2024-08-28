import unittest
from pathlib import Path

from Code.root_path import ROOT_PATH
from Code.systems.texture_validator import (DMSValidator, InvalidSpriteError,
                                            SpriteValidationError)


class TestTextureFolders(unittest.TestCase):
    def setUp(self):
        self.base_path = ROOT_PATH / "Content" / "Sprites"

    def test_validate_all_dms_folders(self):
        try:
            result = DMSValidator.validate_all_dms(self.base_path)
            self.assertTrue(result)
        
        except Exception as err:
            self.fail(str(err))

if __name__ == '__main__':
    unittest.main()
