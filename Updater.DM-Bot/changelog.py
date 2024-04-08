import requests
import yaml
from requests.exceptions import RequestException

from server_info import ServerInfo


class Changelog(ServerInfo):
    def __init__(self) -> None:
        super().__init__()
    
    def get_changelog(self):
        if 'changelog_id' not in self._info_json:
            raise ValueError("\"changelog_id\" not found on server")
        
        response = requests.get(self._url(self._info_json['changelog_id']))
        if response.status_code == 200:
            return yaml.safe_load(response.text)
        else:
            raise RequestException("Error when downloading changelog")

def print_changelog(changelog_info):
    changelog_list = changelog_info.get('changelog', [])
    if not changelog_list:
        print("Не найдено изменений в ченджлоге")
        return

    total_versions = len(changelog_list)
    start_index = 0
    while start_index < total_versions:
        end_index = min(start_index + 10, total_versions)
        for version_info in changelog_list[start_index:end_index]:
            version = version_info.get('version', '█.█.█')
            date = version_info.get('date', '████-██-██')
            changes = version_info.get('changes', [])
            print(f"Версия: {version}")
            print(f"Дата: {date}")
            print("Изменения:")
            for change in changes:
                print(f"  - {change}")
            print()
        if end_index < total_versions:
            choice = input("Хотите продолжить просмотр? (да/нет): ")
            if choice.lower() != "да":
                break
        start_index += 10
