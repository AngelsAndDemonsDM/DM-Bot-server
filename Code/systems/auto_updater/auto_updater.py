import json
import logging
import os
import shutil
import subprocess
import zipfile
from typing import List, Optional, Tuple
import os
import shutil
import logging
from typing import List
import requests
from root_path import ROOT_PATH
class AutoUpdater:
    __slots__ = ['_root_path', '_user', '_repo', '_exclude_dirs', '_merge_dirs', '_user_dir_prefix', '_current_version', '_session', '_remote_version', '_remote_zip_url', '_zip_path']
    
    def __init__(self) -> None:
        self._root_path = ROOT_PATH # Более быстрый доступ и исключаю косяк с возможностью потери данных
        
        with open(os.path.join(self._root_path, "updater_config.json"), 'r') as file:
            config = json.load(file)
        
        self._user = config["USER"]
        self._repo = config["REPO"]
        self._exclude_dirs = config["EXCLUDE_DIRS"]
        self._merge_dirs = config["MERGE_DIRS"]
        self._user_dir_prefix = config["USER_DIR_PREFIX"]
        self._current_version = config["VERSION"]
        self._main_script_path = os.path.join(self._root_path, "Code", "main.py")
        self._session = requests.Session
        self._remote_version = None
        self._remote_zip_url = None
        self._zip_path = os.path.join(self._root_path, "update.zip")
        
    def update_app(self) -> None:
        self._get_remote_data()
        
        if not self._is_needs_update():
            logging.info("Update not need")
            return

        self._download_remote_zip()
        if not os.path.exists(self._zip_path):
            logging.error("zip dosn't download")
            return
        
        self._remove_old_files()
        self._exstract_remote_zip()
        logging.info("done")
        
    def _is_needs_update(self) -> bool:
        if self._remote_version and AutoUpdater._version_tuple(self._current_version) < AutoUpdater._version_tuple(self._remote_version):
            return True
        
        return False
    
    def _get_remote_data(self) -> None:
        response: requests.Response = self._session.get(f"https://api.github.com/repos/{self._user}/{self._repo}/releases/latest")
        if response.status_code == 200:
            try:
                latest_release = response.json()
                self._remote_version = latest_release['tag_name']
                self._remote_zip_url = f"https://github.com/{self._user}/{self._repo}/archive/refs/tags/{self._remote_version}.zip"
                return
            
            except (ValueError, KeyError, AttributeError) as e:
                logging.error(f"Error parsing JSON response: {e}")
                return
        
        logging.error(f"Failed to fetch the latest release information. Status code: {response.status_code}")
        return
    
    @staticmethod
    def _version_tuple(version: str) -> Tuple[int, ...]:
        return tuple(map(int, (version.split("."))))
    
    def _download_remote_zip(self) -> None:
        logging.info(f"Downloading {self._remote_zip_url}")
        with self._session.get(self._remote_zip_url, stream=True) as r:
            with open(self._zip_path, 'wb') as file:
                for chunk in r.iter_content(chunk_size=8192):
                    file.write(chunk)
    
    def _exstract_remote_zip(self) -> None:
        logging.info(f"Extracting {self._zip_path}")
        with zipfile.ZipFile(self._zip_path, 'r') as zip_ref:
            zip_ref.extractall(self._root_path)
        
        logging.info(f"Removing {self._zip_path}")
        os.remove(self._zip_path)
    
    def _remove_old_files(self, script_name: str) -> None:
        def is_user_dir(directory: str, prefix: str) -> bool:
            """Checks if the directory name starts with the user directory prefix."""
            return os.path.basename(directory).startswith(prefix)

        def remove_directory(directory: str) -> None:
            """Removes the specified directory and logs the action."""
            shutil.rmtree(directory)
            logging.info(f"Removed directory: {directory}")

        def remove_file(file: str) -> None:
            """Removes the specified file and logs the action."""
            os.remove(file)
            logging.info(f"Removed file: {file}")

        def clean_subdirectories(directory: str, prefix: str) -> None:
            """Cleans subdirectories within the given directory, excluding user directories."""
            for subitem in os.listdir(directory):
                subitem_path = os.path.join(directory, subitem)
                if os.path.isdir(subitem_path) and not is_user_dir(subitem_path, prefix):
                    remove_directory(subitem_path)
        
        for item in os.listdir(self._root_path):
            item_path = os.path.join(self._root_path, item)
            if item not in self._exclude_dirs and item != script_name and item != "update.zip":
                if os.path.isdir(item_path):
                    if item in self._merge_dirs:
                        clean_subdirectories(item_path, self._user_dir_prefix)
                    
                    else:
                        remove_directory(item_path)
                
                else:
                    remove_file(item_path)

    def _run_main_script(self) -> None:
        subprocess.run(["python", os.path.join(self._root_path, "Code", "main.py")])
