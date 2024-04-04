import os
import sys
import tempfile

import requests
from main_vars import SERVER_INFO_ID, VERSION
from requests.exceptions import RequestException


class Updater:
    def __init__(self) -> None:
        pass
    
    def _get_url(self, id) -> str:
        return f"https://drive.google.com/uc?export=download&id={id}"

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
    
    def get_json_info(self):
        response = requests.get(self._get_url(SERVER_INFO_ID))
        if response.status_code == 200:
            return response.json()
        else:
            raise RequestException("Error when requesting new version")
    
    def is_new_version(self, json_data) -> bool:
        if not 'version' in json_data 
            raise ValueError("\"version\" not found in json_data")
        
        if self.compare_versions(json_data['version'], VERSION) == 1:
            return True
        return False

    def replace_current_file(self, new_file_content):
        current_file_path = sys.executable
        try:
            # Создаем временный файл для новой версии
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(new_file_content)
                temp_file_path = temp_file.name
            # Закрываем текущий исполняемый файл
            os.execv(temp_file_path, sys.argv)
        except Exception as e:
            sys.exit(1) # I'll suck from this later
    
    def download_new_exe(self, json_data):
        if not 'exe_id' in json_data:
            raise ValueError("\"exe_id\" not found in json_data")
        
        response = requests.get(self._get_url(json_data['exe_id']))
        if response.status_code == 200:
            return response.content
        else:
            raise RequestException("Error when download new version")