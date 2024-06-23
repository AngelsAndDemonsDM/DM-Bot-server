import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

from Code.auto_updater.update import (download_and_extract_zip,
                                      get_remote_version_and_zip_url,
                                      load_config, needs_update)


class TestUpdater(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn('VERSION', config)
        self.assertIn('USER', config)
        self.assertIn('REPO', config)

    def test_get_remote_version_and_zip_url(self):
        user = 'test_user'
        repo = 'test_repo'
        
        def mock_requests_get(url):
            class MockResponse:
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code

                def json(self):
                    return self.json_data

            if url == f"https://api.github.com/repos/{user}/{repo}/releases/latest":
                return MockResponse({"tag_name": "v1.0.0"}, 200)
            else:
                return MockResponse(None, 404)
        
        with patch('requests.get', side_effect=mock_requests_get):
            version, zip_url = get_remote_version_and_zip_url(user, repo)
        
        self.assertEqual(version, "v1.0.0")
        self.assertEqual(zip_url, f"https://github.com/{user}/{repo}/archive/refs/tags/v1.0.0.zip")

    def test_download_and_extract_zip(self):
        url = 'https://example.com/test.zip'
        extract_to = self.test_dir
        
        mock_response = MagicMock()
        mock_response.content = b'test content'

        mock_get = MagicMock()
        mock_get.return_value = mock_response

        with patch('requests.get', mock_get):
            extracted_dir = download_and_extract_zip(url, extract_to)
        
        self.assertTrue(os.path.exists(extracted_dir))
        self.assertTrue(os.path.isdir(extracted_dir))

        files_in_dir = os.listdir(extracted_dir)
        self.assertGreater(len(files_in_dir), 0)

    def test_needs_update(self):
        with patch('Code.auto_updater.update.load_config', return_value={"VERSION": "1.0.0", "USER": "test_user", "REPO": "test_repo"}):
            with patch('Code.auto_updater.update.get_remote_version_and_zip_url', return_value=("v2.0.0", "https://example.com/update.zip")):
                needs_update_result = needs_update()
        
        self.assertTrue(needs_update_result[0])
        self.assertEqual(needs_update_result[1], "1.0.0")
        self.assertEqual(needs_update_result[2], "v2.0.0")

if __name__ == '__main__':
    unittest.main()

