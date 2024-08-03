from typing import Any, Dict, Optional

import msgpack
from systems.misc import GlobalClass


class SocketUserAlreadyConnectError(Exception):
    pass


class ConnectManager(GlobalClass):
    __slots__ = ['_initialized', '_connects']
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connects: Dict[str, Any] = {}
    
    @staticmethod
    def _pack_data(data: Any) -> bytes:
        return msgpack.packb(data)
    
    @staticmethod
    def unpack_data(data: bytes) -> Any:
        return msgpack.unpackb(data)
    
    def add_user_connect(self, login: str, websocket: Any) -> None:
        if login in self._connects:
            raise SocketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = websocket
    
    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[Any]:
        return self._connects.get(login, None)
    
    async def send_data(self, login: str, data: Any) -> None:
        websocket = self.get_user_connect(login)
        if websocket:
            packed_data = ConnectManager._pack_data(data)
            await websocket.send(packed_data)
    
    async def broadcast_message(self, data: Any) -> None:
        packed_data = ConnectManager._pack_data(data)
        for websocket in self._connects.values():
            await websocket.send(packed_data)
