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
