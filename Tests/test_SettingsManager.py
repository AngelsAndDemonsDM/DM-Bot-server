import os
import unittest

from Code.db_work.SettingsManager import SettingsManager


class TestSettingsManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.settings_manager = SettingsManager()
        await self.settings_manager.start()

    async def test_create_file(self):
        self.assertTrue(os.path.exists(self.settings_manager._path))

    async def test_set_and_get_setting(self):
        await self.settings_manager.set_setting("theme", "dark")
        theme = await self.settings_manager.get_setting("theme")
        self.assertEqual(theme, "dark")

    async def test_get_nonexistent_setting(self):
        theme = await self.settings_manager.get_setting("nonexistent")
        self.assertIsNone(theme)

    async def test_save_and_load_settings(self):
        settings = {"theme": "dark", "language": "en"}
        await self.settings_manager.save_settings(settings)
        loaded_settings = await self.settings_manager.load_settings()
        self.assertEqual(loaded_settings, settings)

    async def test_overwrite_setting(self):
        await self.settings_manager.set_setting("theme", "dark")
        await self.settings_manager.set_setting("theme", "light")
        theme = await self.settings_manager.get_setting("theme")
        self.assertEqual(theme, "light")

if __name__ == "__main__":
    unittest.main()
