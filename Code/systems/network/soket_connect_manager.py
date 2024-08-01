from asyncio import StreamWriter
from typing import Any, Dict, Optional

from systems.misc import GlobalClass
from systems.network.pakage_deliver_manager import PackageDeliveryManager


class SocketUserAlreadyConnectError(Exception):
    pass

class SocketConnectManager(GlobalClass):
    __slots__ = ['_connects']
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connects: Dict[str, StreamWriter] = {}
    
    def add_user_connect(self, login: str, client_socket: StreamWriter) -> None:
        if login in self._connects:
            raise SocketUserAlreadyConnectError(f"User '{login}' already connected.")
        
        self._connects[login] = client_socket

    def rm_user_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    def get_user_connect(self, login: str) -> Optional[StreamWriter]:
        return self._connects.get(login, None)
    
    async def send_data(self, login: str, data: Any) -> None:
        client_socket = self.get_user_connect(login)
        if client_socket:
            packed_data = PackageDeliveryManager.pack_data(data)
            client_socket.write(packed_data)
            await client_socket.drain()
    
    async def broadcast_data(self, data: Any) -> None:
        packed_data = PackageDeliveryManager.pack_data(data)
        for client_socket in self._connects.values():
            client_socket.write(packed_data)
            await client_socket.drain()
