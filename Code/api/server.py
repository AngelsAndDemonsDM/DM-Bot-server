import json
import os
import zipfile

from api.decorators import server_exception_handler
from quart import Blueprint, jsonify, request, send_file
from root_path import ROOT_PATH

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

@server_exception_handler
@server_bp.route('/download_server_content', methods=['GET'])
async def api_download_server_content():
    zip_path = _create_zip_archive()
    return await send_file(zip_path, mimetype='application/zip', as_attachment=True, attachment_filename="content.zip")
# --- Server content download end --- #

# --- Server check start --- #
CACHED_CONFIG = None

def _load_config():
    global cached_config
    if cached_config is None:
        with open(os.path.join(ROOT_PATH, 'Content', 'updater_config.json'), 'r') as file:
            config_data = json.load(file)
            cached_config = {
                "version":  config_data.get("VERSION", "Unknown"),
                "git_user": config_data.get("USER", "Unknown"),
                "git_repo": config_data.get("REPO", "Unknown")
            }
            
    return cached_config

@server_exception_handler
@server_bp.route('/check_status', methods=['GET'])
async def api_check_status():
    detailed = request.args.get('detailed', default=False, type=bool)

    if detailed:
        response_data = _load_config()
        return jsonify({"message": "Server is online", "detailed": response_data}), 200

    return jsonify({"message": "Server is online"}), 200
# --- Server check end --- #
