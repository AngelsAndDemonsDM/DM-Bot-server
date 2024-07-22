import unittest
from unittest.mock import MagicMock, patch

from quart import Quart
from quart.testing import QuartClient

from Code.api.server import server_bp


class ServerAPITestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    async def asyncSetUpClass(cls):
        cls.app = Quart(__name__)
        cls.app.register_blueprint(server_bp)
        cls.client = cls.app.test_client()

    @patch('Code.api.server._create_zip_archive')
    async def test_api_download_server_content(self, mock_create_zip):
        mock_create_zip.return_value = 'path/to/mock/sprites.zip'

        response = await self.client.get('/download_server_content')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/zip')

    @patch('Code.api.server._load_config')
    async def test_api_check_status_detailed(self, mock_load_config):
        mock_load_config.return_value = {
            "version": "1.0.0",
            "git_user": "test_user",
            "git_repo": "test_repo"
        }

        response = await self.client.get('/check_status?detailed=true')
        
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertIn('detailed', data)
        self.assertEqual(data['detailed']['version'], "1.0.0")

    async def test_api_check_status(self):
        response = await self.client.get('/check_status')
        
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertNotIn('detailed', data)

if __name__ == '__main__':
    unittest.main()
