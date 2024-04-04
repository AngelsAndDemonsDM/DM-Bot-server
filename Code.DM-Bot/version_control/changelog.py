import requests
from requests.exceptions import RequestException
from main_vars import SERVER_INFO_ID

class Changelog:
    def __init__(self):
        pass
    
    def _get_url(self, id) -> str:
        return f"https://drive.google.com/uc?export=download&id={id}"