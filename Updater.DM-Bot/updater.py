import os
import sys

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
