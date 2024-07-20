import json
import os
import unittest

from Code.systems.db_systems import SettingsManager


class TestSettingsManager(unittest.TestCase):
    def setUp(self):
        self.settings_manager = SettingsManager("test_settings")

    def tearDown(self):
        if os.path.exists(self.settings_manager._path):
            os.remove(self.settings_manager._path)

    def test_create_file(self):
        self.settings_manager._create_file()
        self.assertTrue(os.path.exists(self.settings_manager._path))

    def test_load_settings(self):
        self.settings_manager._settings = {'test_key': 'test_value'}
        self.settings_manager._save_settings()
        
        self.settings_manager._settings = {}
        self.settings_manager._load_settings()
        self.assertEqual(self.settings_manager._settings, {'test_key': 'test_value'})

    def test_save_settings(self):
        settings = {'key': 'value'}
        self.settings_manager._settings = settings
        self.settings_manager._save_settings()
        
        with open(self.settings_manager._path, 'r') as file:
            content = json.load(file)
        
        self.assertEqual(content, settings)

    def test_set_setting(self):
        self.settings_manager.set_setting('level1.level2.key', 'value')
        settings = self.settings_manager._load_settings()
        self.assertEqual(settings['level1']['level2']['key'], 'value')

    def test_get_setting(self):
        self.settings_manager._settings = {'level1': {'level2': {'key': 'value'}}}
        self.settings_manager._save_settings()
        value = self.settings_manager.get_setting('level1.level2.key')
        self.assertEqual(value, 'value')

    def test_context_manager(self):
        with SettingsManager("test_settings") as manager:
            manager.set_setting("user.preferences.theme", "dark")
            self.assertEqual(manager.get_setting("user.preferences.theme"), "dark")

        with open(manager._path, 'r') as file:
            content = json.load(file)
        
        self.assertEqual(content["user"]["preferences"]["theme"], "dark")

if __name__ == "__main__":
    unittest.main()
