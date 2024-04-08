import logging
import os
import subprocess
import zipfile

import requests
from requests.exceptions import RequestException

from server_info import ServerInfo


class Updater(ServerInfo):
    def __init__(self, version: str) -> None:
        super().__init__()
        self._version = version

    def compare_versions(self, version1, version2) -> int:
        """
        Сравнивает две строки версий.
        Возвращает 1, если version1 > version2,
                   -1, если version1 < version2,
                   0, если version1 == version2.
        """
        # Разбиваем версии на части и преобразуем их в целые числа
        parts1 = [int(part) for part in version1.split('.')]
        parts2 = [int(part) for part in version2.split('.')]
        
        # Дополняем более короткий список нулями (для случаев 1.2 и 1.2.0)
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
        if not 'version' in self._info_json:
            raise ValueError("\"version\" not found on server")
        
        if self.compare_versions(self._info_json['version'], self._version) == 1:
            return True
        return False

    def download_new_exe(self):
        if not 'exe_id' in self._info_json:
            raise ValueError("\"exe_id\" not found in json_data")
        
        response = requests.get(self._url(self._info_json['exe_id']))
        if response.status_code == 200:
            return response.content
        else:
            raise RequestException("Error when download new version from server")

def check_file_in_directory(directory, filename):
    """
    Проверяет наличие файла в директории.
    """
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        return True
    return False

def check_or_create_directory(directory):
    """
    Проверяет наличие директории.
    Если директория не существует, создает ее.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_version(directory: str = "DM-Bot", filename: str = "DM-Bot.exe") -> str:
    version: str = "0.0.-1"
    check_or_create_directory(directory)
    if check_file_in_directory(directory, filename):
        result = subprocess.run([f"{directory}/{filename}", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
    return version

def update() -> None:
    directory = "DM-Bot"
    exe_filename = "DM-Bot.exe"
    zip_filename = "DM-Bot.zip"

    version = get_version()
    logging.info(f"Текущая версия приложения {version}.")

    updater = Updater(version)
    try:
        is_new: bool = updater.is_new_version()
    except Exception as err:
        logging.error(f"Получена ошибка при попытке считать новую версию с сервера: {err}")
        return

    if not is_new:
        logging.info("Обновлений не обнаружено. У вас самая новая версия DM-Bot.")
        return

    try:
        logging.info("Начинаю скачивать зашифрованный архив с сервера...")
        encrypted_zip_content = updater.download_new_exe()

        encrypted_zip_path = os.path.join(directory, zip_filename)
        with open(encrypted_zip_path, 'wb') as zip_file:
            zip_file.write(encrypted_zip_content)
        logging.info("Архив сохранён!")

        if os.path.exists(exe_filename):
            logging.info("Удаление старого файла DM-Bot.exe")
            os.remove(exe_filename)
         
        logging.info("Начало распаковки...")
        with zipfile.ZipFile(encrypted_zip_path, 'r') as zip_ref:
            zip_ref.extractall(directory, pwd=b"1Ei2ttDIBadNmDHqh3HRIWpipnxh7DwNM")

        logging.info("Архив распакован!")
        os.remove(encrypted_zip_path)

        logging.info("Файл DM-Bot.exe успешно обновлен.")
    except Exception as err:
        logging.error(f"Получена ошибка при попытке обновления: {err}")
        return
