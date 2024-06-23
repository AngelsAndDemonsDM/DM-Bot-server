import json
import os
import shutil
import tempfile
import unittest
from io import BytesIO
from typing import Optional, Tuple
from unittest import mock
from unittest.mock import MagicMock, patch
from zipfile import ZipFile

import requests

from Code.auto_updater.update import *


class TestUpdater(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.app_dir = tempfile.mkdtemp()
        cls.config_file = os.path.join(cls.temp_dir, "updater_config.json")

        config_data = {
            "VERSION": "1.0.0",
            "USER": "test_user",
            "REPO": "test_repo",
            "EXCLUDE_DIRS": [],
            "MERGE_DIRS": [],
            "USER_DIR_PREFIX": "user",
        }
        with open(cls.config_file, 'w') as f:
            json.dump(config_data, f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
        shutil.rmtree(cls.app_dir)

    def test_load_config(self):
        expected_config = {
            "VERSION": "1.0.0",
            "USER": "test_user",
            "REPO": "test_repo",
            "EXCLUDE_DIRS": [],
            "MERGE_DIRS": [],
            "USER_DIR_PREFIX": "user",
        }
        config = load_config(self.config_file)
        self.assertEqual(config, expected_config)

    @patch('my_updater_script.requests.get')
    def test_get_remote_version_and_zip_url_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tag_name": "v2.0.0"}
        mock_get.return_value = mock_response

        version, zip_url = get_remote_version_and_zip_url("test_user", "test_repo")
        self.assertEqual(version, "v2.0.0")
        self.assertEqual(zip_url, "https://github.com/test_user/test_repo/archive/refs/tags/v2.0.0.zip")

    @patch('my_updater_script.requests.get')
    def test_get_remote_version_and_zip_url_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        version, zip_url = get_remote_version_and_zip_url("test_user", "test_repo")
        self.assertIsNone(version)
        self.assertIsNone(zip_url)

    def test_download_and_extract_zip(self):
        zip_content = BytesIO()
        with ZipFile(zip_content, 'w') as zf:
            zf.writestr("test_file.txt", "Test content")

        mock_response = MagicMock()
        mock_response.iter_content.return_value = [zip_content.getvalue()]
        mock_response.status_code = 200

        with patch('my_updater_script.requests.get', return_value=mock_response):
            zip_url = "https://example.com/test.zip"
            extracted_dir = download_and_extract_zip(zip_url, self.temp_dir)

            self.assertTrue(os.path.exists(extracted_dir))
            self.assertTrue(os.path.exists(os.path.join(extracted_dir, "test_file.txt")))

    def test_clean_old_version(self):
        test_dirs = ["dir1", "dir2"]
        test_files = ["file1.txt", "file2.txt"]

        for d in test_dirs:
            os.makedirs(os.path.join(self.app_dir, d))
        for f in test_files:
            open(os.path.join(self.app_dir, f), 'a').close()

        exclude_dirs = []
        merge_dirs = []
        user_dir_prefix = "user"
        script_name = "test_script.py"

        clean_old_version(self.app_dir, exclude_dirs, merge_dirs, user_dir_prefix, script_name)

        for d in test_dirs:
            self.assertFalse(os.path.exists(os.path.join(self.app_dir, d)))
        for f in test_files:
            self.assertFalse(os.path.exists(os.path.join(self.app_dir, f)))

    def test_merge_directories(self):
        src_dir = os.path.join(self.temp_dir, "src")
        dest_dir = os.path.join(self.temp_dir, "dest")

        os.makedirs(src_dir)
        open(os.path.join(src_dir, "file1.txt"), 'a').close()

        merge_directories(src_dir, dest_dir)

        self.assertTrue(os.path.exists(os.path.join(dest_dir, "file1.txt")))

    def test_version_tuple(self):
        version = "1.2.3"
        self.assertEqual(version_tuple(version), (1, 2, 3))

    @patch('my_updater_script.get_remote_version_and_zip_url')
    def test_needs_update(self, mock_get_remote_version):
        mock_get_remote_version.return_value = ("2.0.0", "https://example.com/test.zip")
        with patch('my_updater_script.load_config', return_value={"VERSION": "1.0.0", "USER": "test_user", "REPO": "test_repo"}):
            needs_update_result = needs_update()
            self.assertTrue(needs_update_result[0])
            self.assertEqual(needs_update_result[1], "1.0.0")
            self.assertEqual(needs_update_result[2], "2.0.0")

    @patch('my_updater_script.download_and_extract_zip')
    @patch('my_updater_script.clean_old_version')
    @patch('my_updater_script.merge_directories')
    def test_update_application(self, mock_merge_dirs, mock_clean_old, mock_download_and_extract):
        zip_url = "https://example.com/test.zip"
        temp_dir = os.path.join(self.temp_dir, "temp")
        app_dir = self.app_dir
        exclude_dirs = []
        merge_dirs = []
        user_dir_prefix = "user"
        script_name = "test_script.py"

        mock_download_and_extract.return_value = os.path.join(self.temp_dir, "extracted_dir")

        update_application(zip_url, temp_dir, app_dir, exclude_dirs, merge_dirs, user_dir_prefix, script_name)

        mock_download_and_extract.assert_called_once_with(zip_url, temp_dir)
        mock_clean_old.assert_called_once_with(app_dir, exclude_dirs, merge_dirs, user_dir_prefix, script_name)
        mock_merge_dirs.assert_called_once()

    @patch('my_updater_script.subprocess.run')
    def test_run_main_script(self, mock_subprocess_run):
        main_script = "main_script.py"
        run_main_script(main_script)
        mock_subprocess_run.assert_called_once_with(["python", main_script])

    @patch('my_updater_script.load_config')
    @patch('my_updater_script.get_remote_version_and_zip_url')
    @patch('my_updater_script.update_application')
    @patch('my_updater_script.run_main_script')
    def test_run_update(self, mock_run_main_script, mock_update_application, mock_get_remote_version, mock_load_config):
        mock_load_config.return_value = {
            "USER": "test_user",
            "REPO": "test_repo",
            "EXCLUDE_DIRS": [],
            "MERGE_DIRS": [],
            "USER_DIR_PREFIX": "user",
            "VERSION": "1.0.0",
        }
        mock_get_remote_version.return_value = ("2.0.0", "https://example.com/test.zip")
        main_script = "main_script.py"

        run_update(main_script)

        mock_update_application.assert_called_once_with("https://example.com/test.zip", mock.ANY, mock.ANY, [], [], "user", "updater_script.py")
        mock_run_main_script.assert_called_once_with(main_script)

if __name__ == '__main__':
    unittest.main()
