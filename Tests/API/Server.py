import unittest
import requests
from unittest.mock import patch, MagicMock
from quart import Quart
from quart.testing import QuartClient

# Импортируем серверный Blueprint
from Code.api.server import server_bp

class ServerAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Quart(__name__)
        cls.app.register_blueprint(server_bp)
        cls.client = cls.app.test_client()

    @patch('server._create_zip_archive')
    async def test_api_download_server_content(self, mock_create_zip):
        # Настройка mock-объекта
        mock_create_zip.return_value = 'path/to/mock/sprites.zip'

        response = await self.client.get('/download_server_content')
        
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/zip')

    @patch('server._load_config')
    async def test_api_check_status_detailed(self, mock_load_config):
        # Настройка mock-объекта
        mock_load_config.return_value = {
            "version": "1.0.0",
            "git_user": "test_user",
            "git_repo": "test_repo"
        }

        response = await self.client.get('/check_status?detailed=true')
        
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertIn('detailed', data)
        self.assertEqual(data['detailed']['version'], "1.0.0")

    async def test_api_check_status(self):
        response = await self.client.get('/check_status')
        
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        self.assertEqual(data['message'], "Server is online")
        self.assertNotIn('detailed', data)

if __name__ == '__main__':
    unittest.main()
