import asyncio
import json
import os
import unittest

from Code.db_work import SettingsManager


class TestSettingsManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.settings_manager = SettingsManager("test_settings")

    async def asyncTearDown(self):
        if os.path.exists(self.settings_manager._path):
            os.remove(self.settings_manager._path)

    async def test_create_file(self):
        await self.settings_manager._create_file()
        self.assertTrue(os.path.exists(self.settings_manager._path))

    async def test_load_settings(self):
        await self.settings_manager.save_settings({'test_key': 'test_value'})
        settings = await self.settings_manager.load_settings()
        self.assertEqual(settings, {'test_key': 'test_value'})

    async def test_save_settings(self):
        settings = {'key': 'value'}
        await self.settings_manager.save_settings(settings)
        
        with open(self.settings_manager._path, 'r') as file:
            content = json.load(file)
        
        self.assertEqual(content, settings)

    async def test_set_setting(self):
        await self.settings_manager.set_setting('level1.level2.key', 'value')
        settings = await self.settings_manager.load_settings()
        self.assertEqual(settings['level1']['level2']['key'], 'value')

    async def test_get_setting(self):
        await self.settings_manager.save_settings({'level1': {'level2': {'key': 'value'}}})
        value = await self.settings_manager.get_setting('level1.level2.key')
        self.assertEqual(value, 'value')

if __name__ == "__main__":
    unittest.main()
