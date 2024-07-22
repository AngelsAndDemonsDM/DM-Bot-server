from typing import Dict, Optional

from quart import Websocket


class WebSoketUserAlreadyConnectError(Exception):
    pass

class WebSocketConnectManager:
    __slots__ = ['_connects']
    
    def __init__(self) -> None:
        self._connects: Dict[str, Websocket] = {}
    
    def add_user_connect(self, login: str, websocket: Websocket) -> None:
        if login in self._connects:
            raise WebSoketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = websocket

    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[Websocket]:
        return self._connects.get(login, None)
