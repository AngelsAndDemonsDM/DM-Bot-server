import requests
from requests.exceptions import RequestException

from . import SERVER_INFO_ID


class ServerInfo:
    def __init__(self) -> None:
        self._info_json = self.update_json_info()
    
    def _url(self, id):
        return f"https://drive.google.com/uc?export=download&id={id}"

    def update_json_info(self):
        response = requests.get(self._url(SERVER_INFO_ID))
        if response.status_code == 200:
            return response.json()
        else:
            raise RequestException("Error when requesting new json_info from server")
