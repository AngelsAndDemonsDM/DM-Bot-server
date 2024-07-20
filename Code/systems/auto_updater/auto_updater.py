import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from typing import Tuple

import requests


class AutoUpdater:
    __slots__ = [
        '_root_path',
        '_user',
        '_repo',
        '_exclude_dirs',
        '_merge_dirs',
        '_user_dir_prefix',
        '_current_version',
        '_main_script_path',
        '_session',
        '_remote_version',
        '_remote_zip_url',
        '_zip_path'
    ]
    
    def __init__(self) -> None:
        """Инициализирует AutoUpdater, загружая конфигурацию и устанавливая начальные параметры.
        """
        self._root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, os.pardir))
        
        with open(os.path.join(self._root_path, "updater_config.json"), 'r') as file:
            config = json.load(file)
        
        self._user = config["USER"]
        self._repo = config["REPO"]
        self._exclude_dirs = config["EXCLUDE_DIRS"]
        self._merge_dirs = config["MERGE_DIRS"]
        self._user_dir_prefix = config["USER_DIR_PREFIX"]
        self._current_version = config["VERSION"]
        self._main_script_path = os.path.join(self._root_path, "Code", "main.py")
        self._session = requests.Session()
        self._remote_version = None
        self._remote_zip_url = None
        self._zip_path = os.path.join(self._root_path, "update.zip")
        
    def update_app(self) -> None:
        """Основной метод для обновления приложения.
        Сначала проверяет удаленные данные, затем обновляет приложение, если это необходимо.
        """
        self._get_remote_data()
        
        if not self.is_needs_update():
            logging.info("Update not needed")
            return

        self._download_remote_zip()
        if not os.path.exists(self._zip_path):
            logging.error("Zip file didn't download")
            return
        
        self._remove_old_files()
        self._extract_remote_zip()
        logging.info("Update completed successfully")
        self._run_main_script()
        
    def is_needs_update(self) -> bool:
        """Проверяет, необходимо ли обновление на основе текущей и удаленной версии.

        Returns:
            bool: True, если обновление необходимо, иначе False.
        """
        if self._remote_version and AutoUpdater._version_tuple(self._current_version) < AutoUpdater._version_tuple(self._remote_version):
            return True
        
        return False
    
    def _get_remote_data(self) -> None:
        """Получает данные о последнем выпуске из удаленного репозитория.
        """
        try:
            response = self._session.get(f"https://api.github.com/repos/{self._user}/{self._repo}/releases/latest")
            response.raise_for_status()
        
        except requests.RequestException as e:
            logging.error(f"Failed to fetch the latest release information: {e}")
            return
        
        try:
            latest_release = response.json()
            self._remote_version = latest_release['tag_name']
            self._remote_zip_url = f"https://github.com/{self._user}/{self._repo}/archive/refs/tags/{self._remote_version}.zip"
        
        except (ValueError, KeyError, AttributeError) as e:
            logging.error(f"Error parsing JSON response: {e}")
    
    @staticmethod
    def _version_tuple(version: str) -> Tuple[int, ...]:
        """Преобразует строку версии в кортеж целых чисел для сравнения.

        Args:
            version (str): Строка версии.

        Returns:
            Tuple[int, ...]: Кортеж с частями версии как целыми числами.
        """
        return tuple(map(int, (version.split("."))))
    
    def _download_remote_zip(self) -> None:
        """Скачивает zip-архив с обновлением из удаленного репозитория.
        """
        logging.info(f"Downloading {self._remote_zip_url}")
        try:
            with self._session.get(self._remote_zip_url, stream=True) as r:
                r.raise_for_status()
                with open(self._zip_path, 'wb') as file:
                    for chunk in r.iter_content(chunk_size=8192):
                        file.write(chunk)
        
        except requests.RequestException as e:
            logging.error(f"Failed to download the zip file: {e}")
    
    def _extract_remote_zip(self) -> None:
        """Извлекает скачанный zip-архив и удаляет его после извлечения.
        Если в архиве содержится одна папка, извлекает только ее содержимое.
        """
        logging.info(f"Extracting {self._zip_path}")
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with zipfile.ZipFile(self._zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                
                extracted_items = os.listdir(tmpdirname)
                if len(extracted_items) == 1 and os.path.isdir(os.path.join(tmpdirname, extracted_items[0])):
                    source_dir = os.path.join(tmpdirname, extracted_items[0])
                    for item in os.listdir(source_dir):
                        src_path = os.path.join(source_dir, item)
                        dest_path = os.path.join(self._root_path, item)
                        if os.path.isdir(src_path):
                            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src_path, dest_path)
                else:
                    for item in extracted_items:
                        src_path = os.path.join(tmpdirname, item)
                        dest_path = os.path.join(self._root_path, item)
                        if os.path.isdir(src_path):
                            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src_path, dest_path)
        
            logging.info(f"Removing {self._zip_path}")
            os.remove(self._zip_path)
        except zipfile.BadZipFile as e:
            logging.error(f"Failed to extract the zip file: {e}")
        
        except shutil.Error as e:
            logging.error(f"Failed to move files: {e}")
    
    def _remove_old_files(self) -> None:
        """Удаляет старые файлы и директории, исключая указанные в конфигурации и пользовательские директории.
        """
        def is_user_dir(directory: str, prefix: str) -> bool:
            """Проверяет, начинается ли имя директории с префикса пользовательской директории.

            Args:
                directory (str): Имя директории.
                prefix (str): Префикс пользовательской директории.

            Returns:
                bool: True, если директория является пользовательской, иначе False.
            """
            return os.path.basename(directory).startswith(prefix)

        def remove_directory(directory: str) -> None:
            """Удаляет директорию и логирует это действие.

            Args:
                directory (str): Путь к директории.
            """
            shutil.rmtree(directory)
            logging.info(f"Removed directory: {directory}")

        def remove_file(file: str) -> None:
            """Удаляет файл и логирует это действие.

            Args:
                file (str): Путь к файлу.
            """
            os.remove(file)
            logging.info(f"Removed file: {file}")

        def clean_subdirectories(directory: str, prefix: str) -> None:
            """Очищает поддиректории в указанной директории, исключая пользовательские директории.

            Args:
                directory (str): Путь к директории.
                prefix (str): Префикс пользовательской директории.
            """
            for subitem in os.listdir(directory):
                subitem_path = os.path.join(directory, subitem)
                if os.path.isdir(subitem_path) and not is_user_dir(subitem_path, prefix):
                    remove_directory(subitem_path)
        
        for item in os.listdir(self._root_path):
            item_path = os.path.join(self._root_path, item)
            if item not in self._exclude_dirs and item != os.path.basename(__file__) and item != "update.zip":
                if os.path.isdir(item_path):
                    if item in self._merge_dirs:
                        clean_subdirectories(item_path, self._user_dir_prefix)
                    
                    else:
                        remove_directory(item_path)
                
                else:
                    remove_file(item_path)

    def _run_main_script(self) -> None:
        """Запускает основной скрипт приложения.
        """
        logging.info(f"Running main script: {self._main_script_path}")
        subprocess.run(["python", self._main_script_path])

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    updater = AutoUpdater()
    updater.update_app()
    sys.exit(0)
    