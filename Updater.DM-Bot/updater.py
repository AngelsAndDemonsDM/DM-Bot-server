import logging
import os
import shutil
import subprocess

import pyzipper
import requests
from requests.exceptions import RequestException
from server_info import ServerInfo


class Updater(ServerInfo):
    def __init__(self) -> None:
        super().__init__()
        self._version = self.get_version()

    @property
    def version(self) -> str:
        return self._version

    def compare_versions(self, version1: str, version2: str) -> int:
        if not version1 and not version2:
            return 0
        
        if not version1:
            return -1
        
        if not version2:
            return 1
        
        parts1 = [int(part) for part in version1.split('.')]
        parts2 = [int(part) for part in version2.split('.')]
        
        len_diff = len(parts1) - len(parts2)
        if len_diff > 0:
            parts2 += [0] * len_diff
        elif len_diff < 0:
            parts1 += [0] * (-len_diff)
        
        for part1, part2 in zip(parts1, parts2):
            if part1 > part2:
                return 1
            elif part1 < part2:
                return -1
        return 0
    
    def is_new_version(self) -> bool:
        if 'version' not in self._info_json:
            raise ValueError("\"version\" not found on server")
        
        if self.compare_versions(self._info_json['version'], self._version) == 1:
            return True
        return False

    def download(self, file_name, chunk_size=8192, retries=3, timeout=30):
        if 'download' not in self._info_json:
            raise ValueError("\"download\" not found in json_data")
        
        for _ in range(retries):
            try:
                with requests.get(self._url(self._info_json['download']), stream=True, timeout=timeout) as response:
                    response.raise_for_status()
                    
                    with open(file_name, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                file.write(chunk)
                
                return file_name
            
            except requests.Timeout:
                print(f"Timeout occurred during download. Retrying ({retries} retries left).")
            except requests.RequestException as e:
                print(f"Error during download: {e}. Retrying ({retries} retries left).")
        
        raise RequestException(f"Failed to download after {retries} retries.")

    def update(self):
        destination_folder = "DM-Bot"
        zip_filename = "DM-Bot.zip"

        self._version = self.get_version

        try:
            is_new = self.is_new_version()
        except Exception as err:
            logging.error(f"Получена ошибка при попытке считать новую версию с сервера: {err}")
            return

        if not is_new:
            logging.info("Обновлений не обнаружено. У вас самая новая версия DM-Bot.")
            return

        try:
            if os.path.exists(destination_folder):
                logging.info("Удаление старой версии")
                shutil.rmtree(destination_folder)

            logging.info("Начинаю скачивать зашифрованный архив с сервера...")
            self.download(file_name=zip_filename)
            
            logging.info("Начало распаковки...")
            with pyzipper.AESZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.setpassword(b"1Ei2ttDIBadNmDHqh3HRIWpipnxh7DwNM")
                zip_ref.extractall(os.getcwd())

            logging.info("Архив распакован!")
            os.remove(zip_filename)

            logging.info("Программа успешно обновлена")
        except Exception as err:
            logging.error(f"Получена ошибка при попытке обновления: {err}")
            return

    @staticmethod
    def check_file_in_directory(directory, filename):
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            return True
        return False

    @staticmethod
    def get_version(directory: str = "DM-Bot", filename: str = "main.exe") -> str:
        version = None

        if Updater.check_file_in_directory(directory, filename):
            result = subprocess.run([f"{directory}/{filename}", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()

        return version
