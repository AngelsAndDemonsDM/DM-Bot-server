import json
import os
import unittest

from quart import Quart

from Code.api.server import (api_check_status, api_download_server_content,
                             server_bp)
from Code.root_path import ROOT_PATH


class ServerAPITestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = Quart(__name__)
        self.app.register_blueprint(server_bp)
        self.client = self.app.test_client()

        self.test_root_path = 'test_root'
        self.sprites_folder = os.path.join(self.test_root_path, 'Sprites')
        self.data_folder = os.path.join(self.test_root_path, 'data')
        os.makedirs(self.sprites_folder, exist_ok=True)
        os.makedirs(self.data_folder, exist_ok=True)
        
        self.test_file_path = os.path.join(self.sprites_folder, 'test.txt')
        with open(self.test_file_path, 'w') as f:
            f.write("Test content")

        self.config_file_path = os.path.join(self.test_root_path, 'updater_config.json')
        with open(self.config_file_path, 'w') as f:
            config_data = {
                "VERSION": "1.0.0",
                "USER": "test_user",
                "REPO": "test_repo"
            }
            json.dump(config_data, f)

        global ROOT_PATH
        self.original_root_path = ROOT_PATH
        ROOT_PATH = self.test_root_path

    async def asyncTearDown(self):
        for root, dirs, files in os.walk(self.test_root_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_root_path)
        
        global ROOT_PATH
        ROOT_PATH = self.original_root_path

    async def test_api_download_server_content(self):
        response = await self.client.get('/download_server_content')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/zip')

    async def test_api_check_status_detailed(self):
        response = await self.client.get('/check_status?detailed=true')
        
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertIn('detailed', data)
        self.assertEqual(data['detailed']['version'], "1.0.0")
        self.assertEqual(data['detailed']['git_user'], "test_user")
        self.assertEqual(data['detailed']['git_repo'], "test_repo")

    async def test_api_check_status(self):
        response = await self.client.get('/check_status')
        
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertNotIn('detailed', data)

if __name__ == '__main__':
    unittest.main()
