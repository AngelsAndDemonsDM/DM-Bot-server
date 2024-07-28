import os
import zipfile

from api.decorators import server_exception_handler
from quart import Blueprint, jsonify, send_file
from root_path import ROOT_PATH
from systems.db_systems import MainSettings
server_bp = Blueprint('server', __name__)

# --- Server content download start --- #
def _get_latest_modification_time(directory_path: str) -> float:
    """Получает время последней модификации файлов в директории.

    Args:
        directory_path (str): Путь к директории.

    Returns:
        float: Время последней модификации в формате timestamp.
    """
    latest_time = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_time = os.path.getmtime(file_path)
            if file_time > latest_time:
                latest_time = file_time
    
    return latest_time

def _create_zip_archive() -> str:
    """Создает ZIP-архив из папки 'Content' и возвращает путь к архиву.

    Проверяет время последней модификации файлов перед пересозданием.

    Returns:
        str: Путь к созданному ZIP-архиву.
    """
    folder_path = os.path.join(ROOT_PATH, "Content")
    archive_path = os.path.join(ROOT_PATH, "data", "content.zip")

    directory_latest_time = _get_latest_modification_time(folder_path)

    if os.path.exists(archive_path):
        archive_time = os.path.getmtime(archive_path)
        if archive_time >= directory_latest_time:
            return archive_path
        
        else:
            os.remove(archive_path)
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    
    return archive_path

@server_bp.route('/download_server_content', methods=['GET'])
@server_exception_handler
async def api_download_server_content():
    zip_path = _create_zip_archive()
    if not zipfile.is_zipfile(zip_path):
        return jsonify({"error": "Internal Server Error"}), 500

    return await send_file(zip_path, mimetype='application/zip', as_attachment=True, attachment_filename="content.zip")
# --- Server content download end --- #

# --- Server check start --- #
@server_bp.route('/check_status', methods=['GET'])
@server_exception_handler
async def api_check_status():
    config: MainSettings = MainSettings.get_instance()
    server_name = config.get_setting("server.name")
    host = config.get_setting("server.ip")
    port = config.get_setting("server.http_port")
    socket_port = config.get_setting("server.socket_port")
    
    if not all([host, port, socket_port]):
        return jsonify({"message": "Server configuration is incomplete"}), 500
        
    server_info = {
        "server_name": server_name,
        "host": host,
        "http_port": port,
        "socket_port": socket_port
    }
    
    return jsonify({"message": "Server is online", "server_info": server_info}), 200
# --- Server check end --- #
