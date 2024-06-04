import asyncio
import json
import os
import unittest

import aiofiles

from Code.db_work import SettingsManager


class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), 'test_data')
        self.test_file = os.path.join(self.test_dir, 'main_settings.json')
        
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        self.settings_manager = SettingsManager()
        self.settings_manager._path = self.test_file

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_create_file(self):
        async def run_test():
            result = await self.settings_manager._create_file()
            self.assertTrue(result)
            self.assertTrue(os.path.exists(self.test_file))

            result = await self.settings_manager._create_file()
            self.assertFalse(result)

        asyncio.run(run_test())

    def test_load_settings(self):
        async def run_test():
            await self.settings_manager._create_file()
            settings = await self.settings_manager.load_settings()
            self.assertEqual(settings, {})

            async with aiofiles.open(self.test_file, "w") as file:
                await file.write(json.dumps({'key': 'value'}))

            settings = await self.settings_manager.load_settings()
            self.assertEqual(settings, {'key': 'value'})

        asyncio.run(run_test())

    def test_save_settings(self):
        async def run_test():
            settings = {'key': 'value'}
            await self.settings_manager.save_settings(settings)

            async with aiofiles.open(self.test_file, "r") as file:
                content = await file.read()
                saved_settings = json.loads(content)

            self.assertEqual(saved_settings, settings)

        asyncio.run(run_test())

    def test_set_setting(self):
        async def run_test():
            await self.settings_manager.set_setting('bot.some_field.value', 'new_value')
            settings = await self.settings_manager.load_settings()
            self.assertEqual(settings['bot']['some_field']['value'], 'new_value')

        asyncio.run(run_test())

    def test_get_setting(self):
        async def run_test():
            await self.settings_manager.set_setting('bot.some_field.value', 'new_value')
            value = await self.settings_manager.get_setting('bot.some_field.value')
            self.assertEqual(value, 'new_value')

            value = await self.settings_manager.get_setting('bot.non_existent_field')
            self.assertIsNone(value)

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
