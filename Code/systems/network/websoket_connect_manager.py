from typing import Any, Dict, Optional

import msgpack
from quart import Websocket


class WebSoketUserAlreadyConnectError(Exception):
    pass

class WebSocketConnectManager:
    __slots__ = ['_connects']
    
    def __init__(self) -> None:
        self._connects: Dict[str, Websocket] = {}
    
    @staticmethod
    def _dump_data(data: Any) -> bytes:
        return msgpack.packb(data)
    
    def add_user_connect(self, login: str, websocket: Websocket) -> None:
        if login in self._connects:
            raise WebSoketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = websocket

    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[Websocket]:
        return self._connects.get(login, None)
    
    async def send_data(self, login: str, data: Any) -> None:
        websocket = self.get_user_connect(login)
        if websocket:
            await websocket.send(WebSocketConnectManager._dump_data(data))
    
    async def broadcast_data(self, data: Any) -> None:
        data = WebSocketConnectManager._dump_data(data)
        for websocket in self._connects.values():
            await websocket.send(data)
