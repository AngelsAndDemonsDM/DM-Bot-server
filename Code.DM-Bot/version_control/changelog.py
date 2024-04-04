import requests
import yaml
from requests.exceptions import RequestException
from version_control.server_info import ServerInfo


class Changelog(ServerInfo):
    def __init__(self) -> None:
        super().__init__()
    
    def get_changelog(self):
        if not 'changelog_id' in self._info_json:
            raise ValueError("\"changelog_id\" not found on server")
        
        response = requests.get(self._url(self._info_json['changelog_id']))
        if response.status_code == 200:
            try:
                return yaml.safe_load(response.text)
            except yaml.YAMLError as exc:
                raise RequestException(f"Failed to parse the changelog {exc}")
        else:
            raise RequestException("Error when downloading changelog")