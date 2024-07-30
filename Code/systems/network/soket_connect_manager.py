import socket
from typing import Any, Dict, Optional

import msgpack
from systems.misc import GlobalClass


class SocketUserAlreadyConnectError(Exception):
    pass

class SocketConnectManager(GlobalClass):
    __slots__ = ['_connects']
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connects: Dict[str, Any] = {}
    
    @staticmethod
    def pack_data(data: Any) -> bytes:
        return msgpack.packb(data)
    
    @staticmethod
    def unpack_data(data: bytes) -> Any:
        return msgpack.unpackb(data, raw=False)
    
    def add_user_connect(self, login: str, client_socket: Any) -> None:
        if login in self._connects:
            raise SocketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = client_socket

    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[Any]:
        return self._connects.get(login, None)
    
    async def send_data(self, login: str, data: Any) -> None:
        client_socket = self.get_user_connect(login)
        if client_socket:
            packed_data = SocketConnectManager.pack_data(data)
            client_socket.write(packed_data)
            await client_socket.drain()
    
    async def broadcast_data(self, data: Any) -> None:
        packed_data = SocketConnectManager.pack_data(data)
        for client_socket in self._connects.values():
            client_socket.write(packed_data)
            await client_socket.drain()
