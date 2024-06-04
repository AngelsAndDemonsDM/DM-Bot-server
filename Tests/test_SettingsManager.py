import asyncio
import os
import unittest

from Code.db_work.SettingsManager import SettingsManager

class TestSettingsManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.settings_manager = SettingsManager()
        if os.path.exists(self.settings_manager._path):
            os.remove(self.settings_manager._path)
        
        await asyncio.wait_for(self.settings_manager._create_file(), timeout=5)

    async def asyncTearDown(self):
        if os.path.exists(self.settings_manager._path):
            os.remove(self.settings_manager._path)
        
        if os.path.exists(os.path.dirname(self.settings_manager._path)):
            os.rmdir(os.path.dirname(self.settings_manager._path))

    async def test_create_file(self):
        await asyncio.wait_for(self.settings_manager._create_file(), timeout=5)
        self.assertTrue(os.path.exists(self.settings_manager._path))

    async def test_set_and_get_setting(self):
        await asyncio.wait_for(self.settings_manager.set_setting("theme", "dark"), timeout=5)
        theme = await asyncio.wait_for(self.settings_manager.get_setting("theme"), timeout=5)
        self.assertEqual(theme, "dark")

    async def test_set_and_get_nested_setting(self):
        await asyncio.wait_for(self.settings_manager.set_setting("bot.some_field.value", "new_value"), timeout=5)
        value = await asyncio.wait_for(self.settings_manager.get_setting("bot.some_field.value"), timeout=5)
        self.assertEqual(value, "new_value")

    async def test_get_nonexistent_setting(self):
        theme = await asyncio.wait_for(self.settings_manager.get_setting("nonexistent"), timeout=5)
        self.assertIsNone(theme)

    async def test_save_and_load_settings(self):
        settings = {"theme": "dark", "language": "en"}
        await asyncio.wait_for(self.settings_manager.save_settings(settings), timeout=5)
        loaded_settings = await asyncio.wait_for(self.settings_manager.load_settings(), timeout=5)
        self.assertEqual(loaded_settings, settings)

    async def test_overwrite_setting(self):
        await asyncio.wait_for(self.settings_manager.set_setting("theme", "dark"), timeout=5)
        await asyncio.wait_for(self.settings_manager.set_setting("theme", "light"), timeout=5)
        theme = await asyncio.wait_for(self.settings_manager.get_setting("theme"), timeout=5)
        self.assertEqual(theme, "light")

if __name__ == "__main__":
    unittest.main()
