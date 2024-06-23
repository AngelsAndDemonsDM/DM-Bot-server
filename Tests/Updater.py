import json
import os
import shutil
import tempfile
import unittest
from io import BytesIO
from zipfile import ZipFile

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

    def test_get_remote_version_and_zip_url_success(self):
        version = "v2.0.0"
        zip_url = "https://github.com/test_user/test_repo/archive/refs/tags/v2.0.0.zip"
        self.assertEqual(get_remote_version_and_zip_url("test_user", "test_repo"), (version, zip_url))

    def test_get_remote_version_and_zip_url_failure(self):
        self.assertIsNone(get_remote_version_and_zip_url("invalid_user", "invalid_repo"))

    def test_download_and_extract_zip(self):
        zip_content = BytesIO()
        with ZipFile(zip_content, 'w') as zf:
            zf.writestr("test_file.txt", "Test content")

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

    def test_needs_update(self):
        self.assertTrue(needs_update())

    def test_update_application(self):
        zip_url = "https://example.com/test.zip"
        temp_dir = os.path.join(self.temp_dir, "temp")
        exclude_dirs = []
        merge_dirs = []
        user_dir_prefix = "user"
        script_name = "test_script.py"

        update_application(zip_url, temp_dir, self.app_dir, exclude_dirs, merge_dirs, user_dir_prefix, script_name)

        # Add assertions for update_application if needed

    def test_run_main_script(self):
        main_script = "main_script.py"
        run_main_script(main_script)

        # Add assertions for run_main_script if needed

    def test_run_update(self):
        main_script = "main_script.py"
        run_update(main_script)

        # Add assertions for run_update if needed

if __name__ == '__main__':
    unittest.main()
