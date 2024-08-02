import logging
import zipfile
from asyncio import StreamReader, StreamWriter
from pathlib import Path
from typing import Any, Dict, Optional

from root_path import ROOT_PATH
from systems.db_systems import UniqueConstraintError
from systems.events_system import EventManager
from systems.misc import GlobalClass
from systems.network import (AccessError, AuthError, PackageDeliveryManager,
                             UserAuth)

logger = logging.getLogger("Socket Server")

class SocketUserAlreadyConnectError(Exception):
    pass

class SoketServerSystem(GlobalClass):
    __slots__ = ['_connects']
    
    DEFAULT_BUFFER: int = 8192
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connects: Dict[str, StreamWriter] = {}

    # Менеджмент коннектов
    def _add_connect(self, login: str, client_socket: StreamWriter) -> None:
        self._connects[login] = client_socket

    def _remove_connect(self, login: str) -> None:
        self._connects.pop(login, None)
    
    # Отправка данных через StreamWriter
    @staticmethod
    async def _send_data_viva_writer(writer: StreamWriter, data: Any) -> None:
        if not data:
            raise ValueError("Send empty data")
        
        writer.write(PackageDeliveryManager.pack_data(data))
        await writer.drain()

    @staticmethod
    async def _send_response_viva_writer(writer: StreamWriter, data: Any) -> None:
        if not data:
            raise ValueError("Send empty response data")
        
        writer.write(PackageDeliveryManager.pack_data(data))
        await writer.drain()
        
        writer.close()
        await writer.wait_closed()

    # Публичное API
    def get_user(self, login: str) -> Optional[StreamWriter]:
        return self._connects.get(login)
    
    async def send_data(self, login: str, data: Any) -> None:
        writer = self.get_user(login)
        if writer:
            await self._send_data_viva_writer(writer, data)
    
    async def broadcast_data(self, data: Any) -> None:
        packed_data = PackageDeliveryManager.pack_data(data)
        for writer in self._connects.values():
            writer.write(packed_data)
            await writer.drain()

    # Обработка клиента
    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        user_auth = UserAuth()
        event_manager = EventManager()
        user = None
        try:
            user_data = await reader.read(self.DEFAULT_BUFFER)
            user_data = PackageDeliveryManager.unpack_data(user_data)
            if not isinstance(user_data, str):
                await self._send_response_viva_writer(writer, "Forbidden. Only str commands")
                return
            
            command = user_data.split()[0]
            match command:
                case "status":
                    await self._send_response_viva_writer(writer, "OK")
                
                case "download":           
                    await self.download(user_data, writer)
                
                case "auth":
                    await self.auth(user_data, writer)
                
                case "token":
                    token = user_data.split()[1]
                    if not token:
                        await self._send_response_viva_writer(writer, "Missing token")
                        return

                    user, access = await user_auth.get_login_access_by_token(token)

                    self._add_connect(user, writer)

                    await self._send_data_viva_writer(writer, "Token accepted")

                    while True:
                        message_data = await reader.read(self.DEFAULT_BUFFER)
                        if not message_data:
                            break

                        try:
                            message_data = PackageDeliveryManager.unpack_data(message_data)
                            if not isinstance(message_data, dict):
                                await self._send_data_viva_writer(writer, "Invalid data")
                            
                            event_type = message_data.get("ev_type")
                            await event_manager.call_event(event_type, socket_user=user, socket_access=access, **message_data)

                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                            
                case _:
                    await self._send_response_viva_writer(writer, "Forbidden. Unknown command")
        
        except AuthError:
            await self._send_response_viva_writer(writer, "Unauthorized")
        
        except AccessError:
            await self._send_response_viva_writer(writer, "Forbidden")
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        finally:
            if user:
                await user_auth.logout(user)
                self._remove_connect(user)
            
            writer.write_eof()
            await writer.drain()

    async def download(self, user_data: str, writer: StreamWriter) -> None:
        args = user_data.split()
        if args and args[1] == "gd":
            await self._send_response_viva_writer(writer, _get_mod_time())
            return
        
        zip_path = _create_zip_archive()
        if not zipfile.is_zipfile(zip_path):
            await self._send_response_viva_writer(writer, "Internal Server Error")
            return
        
        # Чтение и отправка файла через сокет
        with open(zip_path, 'rb') as zip_file:
            while data := zip_file.read(self.DEFAULT_BUFFER):
                writer.write(data)
                await writer.drain()
        
        writer.write_eof()
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    
    async def auth(self, user_data: str, writer: StreamWriter) -> None:
        args = user_data.split()
        if len(args) < 4:
            await self._send_response_viva_writer(writer, "Forbidden. Unknown command")
            return
        
        command, login, password = args[1:4]
        user_auth = UserAuth()
        
        if command == "lin":
            if not login or not password:
                await self._send_response_viva_writer(writer, "Login and password are required")
                return
        
            try:
                token = await user_auth.login_user(login, password)
                await self._send_response_viva_writer(writer, token)
            
            except AuthError:
                await self._send_response_viva_writer(writer, "Invalid credentials")
        
        elif command == "reg":
            if not login or not password:
                await self._send_response_viva_writer(writer, "Login and password are required")
                return
                
            try:
                await user_auth.register_user(login, password)
                await self._send_response_viva_writer(writer, "User registered successfully")
            except UniqueConstraintError:
                await self._send_response_viva_writer(writer, "Login already exists")
        
        else:
            await self._send_response_viva_writer(writer, "Forbidden. Unknown command")
    
def _get_mod_time() -> float:
    root_path = Path(ROOT_PATH)
    return _get_latest_modification_time(root_path / "Content")

def _get_latest_modification_time(directory_path: str) -> float:
    """Получает время последней модификации файлов в директории.

    Args:
        directory_path (str): Путь к директории.

    Returns:
        float: Время последней модификации в формате timestamp.
    """
    directory = Path(directory_path)
    latest_time = max((file.stat().st_mtime for file in directory.rglob('*') if file.is_file()), default=0)
    return latest_time

def _create_zip_archive() -> str:
    """Создает ZIP-архив из папки 'Content' и возвращает путь к архиву.

    Проверяет время последней модификации файлов перед пересозданием.

    Returns:
        str: Путь к созданному ZIP-архиву.
    """
    root_path = Path(ROOT_PATH)
    folder_path = root_path / "Content"
    archive_path = root_path / "data" / "content.zip"

    directory_latest_time = _get_latest_modification_time(folder_path)

    if archive_path.exists() and archive_path.stat().st_mtime >= directory_latest_time:
        return str(archive_path)
    
    archive_path.unlink(missing_ok=True)
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in folder_path.rglob('*'):
            if file.is_file():
                zipf.write(file, file.relative_to(folder_path))
    
    return str(archive_path)
