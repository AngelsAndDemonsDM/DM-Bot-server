import logging
import zipfile
from asyncio import StreamReader, StreamWriter
from pathlib import Path
from typing import Any, Dict, Optional

from root_path import ROOT_PATH
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
        if login in self._connects:
            del self._connects[login]
            
        self._connects[login] = client_socket # На похуях перезаписываем

    def _remove_connect(self, login: str) -> None:
        if login in self._connects:
            del self._connects[login]
    
    # Отправка данных через StreamWriter
    @staticmethod
    async def _send_data_viva_writer(writer: StreamWriter, data: Any) -> None:
        if not data:
            raise ValueError(f"Send empty data")    
        
        writer.write(PackageDeliveryManager.pack_data(data))
        await writer.drain()

    @staticmethod
    async def _send_response_viva_writer(writer: StreamWriter, data: Any) -> None:
        if not data:
            raise ValueError(f"Send empty response data")    
        
        writer.write(PackageDeliveryManager.pack_data(data))
        await writer.drain()
        
        writer.close()
        await writer.wait_closed()

    # Публичное api
    def get_user(self, login: str) -> Optional[StreamWriter]:
        return self._connects.get(login, None)
    
    async def send_data(self, login: str, data: Any) -> None:
        writer = self.get_user(login)
        if writer:
            await self._send_data_viva_writer(writer, data)
    
    async def broadcast_data(self, data: Any) -> None:
        packed_data = PackageDeliveryManager.pack_data(data)
        for writer in self._connects.values():
            writer.write(packed_data)
            await writer.drain()

    # Используете вне main.py - кастрирую
    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        user = None
        try:
            user_data = reader.read(self.DEFAULT_BUFFER)
            user_data = PackageDeliveryManager.unpack_data(user_data)
            if not isinstance(user_data, str):
                await SoketServerSystem._send_response_viva_writer(writer, b"Forbidden. Only str commands")
            
            match user_data.split()[0]:
                case "status":
                    await SoketServerSystem._send_response_viva_writer(writer, b"OK")
                
                case "download":           
                    await self.download(user_data, writer)
                
                case "auth":
                    await self.auth(user_data, writer)
                
                case "admin":
                    pass
                
                case "token":
                    pass
                
                case _:
                    await SoketServerSystem._send_response_viva_writer(writer, b"Forbidden. Unknown command")
                

        except AuthError:
            await SoketServerSystem._send_response_viva_writer(writer, b"Unauthorized")
        
        except AccessError:
            await SoketServerSystem._send_response_viva_writer(writer, b"Forbidden")
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        finally:
            if user:
                self._remove_connect(user)
            
            writer.write()
            await writer.drain()

    async def download(self, user_data: str, writer: StreamWriter) -> None:
        args = user_data.split()
        if args and args[1] == "get_data":
            await self._send_response_viva_writer(writer, _get_mod_time())
        
        else:
            zip_path = _create_zip_archive()
            if not zipfile.is_zipfile(zip_path):
                await SoketServerSystem._send_response_viva_writer(writer, b"Internal Server Error")
                return
            
            # Чтение и отправка файла через сокет
            with open(zip_path, 'rb') as zip_file:
                while True:
                    data = zip_file.read(SoketServerSystem.DEFAULT_BUFFER)
                    if not data:
                        break
                    writer.write(data)
                    await writer.drain()
            
            writer.write_eof()
            await writer.drain()
            writer.close()
            await writer.wait_closed()
    
    async def auth(self, user_data: str, writer: StreamWriter) -> None:
        pass
    
    async def admin(self, user_data: str, writer: StreamWriter) -> None:
        pass

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
    latest_time = 0
    for file in directory.rglob('*'):
        if file.is_file():
            file_time = file.stat().st_mtime
            if file_time > latest_time:
                latest_time = file_time
    
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

    if archive_path.exists():
        archive_time = archive_path.stat().st_mtime
        if archive_time >= directory_latest_time:
            return str(archive_path)
        
        else:
            archive_path.unlink()
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in folder_path.rglob('*'):
            if file.is_file():
                zipf.write(file, file.relative_to(folder_path))
    
    return str(archive_path)
