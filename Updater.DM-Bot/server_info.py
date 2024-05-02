import requests
import requests.sessions

SERVER_INFO_ID: str = "1_Ytb9xGDPerlInZmWtPrC06MKSglF_8g"

class ServerInfo:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._info_json = self.update_json_info()

    def _url(self, id: str) -> str:
        return f"https://drive.google.com/uc?export=download&id={id}"

    def update_json_info(self):
        with self._session.get(self._url(SERVER_INFO_ID)) as response:
            response.raise_for_status()

            return response.json()

    def raise_if_not_data(self, key: str) -> None:
        if key not in self._info_json:
            raise ValueError(f"\"{key}\" not found in json_data")