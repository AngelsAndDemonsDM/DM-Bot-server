import socket
from typing import Any, Dict, Optional

import msgpack
from systems.decorators import global_class


class SocketUserAlreadyConnectError(Exception):
    pass

@global_class
class SocketConnectManager:
    __slots__ = ['_connects']
    
    def __init__(self) -> None:
        self._connects: Dict[str, socket.socket] = {}
    
    @staticmethod
    def pack_data(data: Any) -> bytes:
        return msgpack.packb(data)
    
    @staticmethod
    def unpack_data(data: bytes) -> Any:
        return msgpack.unpackb(data, raw=False)
    
    def add_user_connect(self, login: str, client_socket: socket.socket) -> None:
        if login in self._connects:
            raise SocketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = client_socket

    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[socket.socket]:
        return self._connects.get(login, None)
    
    def send_data(self, login: str, data: Any) -> None:
        client_socket = self.get_user_connect(login)
        if client_socket:
            client_socket.send(SocketConnectManager.pack_data(data))
    
    def broadcast_data(self, data: Any) -> None:
        data = SocketConnectManager.pack_data(data)
        for client_socket in self._connects.values():
            client_socket.send(data)
