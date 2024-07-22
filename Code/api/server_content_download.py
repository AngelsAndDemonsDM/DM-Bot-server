import os
import zipfile

from quart import request, send_file
from root_path import ROOT_PATH


def get_latest_modification_time(directory_path: str) -> float:
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

def create_zip_archive() -> str:
    """Создает ZIP-архив из папки 'Sprites' и возвращает путь к архиву.

    Проверяет время последней модификации файлов перед пересозданием.

    Returns:
        str: Путь к созданному ZIP-архиву.
    """
    folder_path = os.path.join(ROOT_PATH, "Sprites")
    archive_path = os.path.join(ROOT_PATH, "data", "sprites.zip")

    directory_latest_time = get_latest_modification_time(folder_path)

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

@server_bp.route('/download_server_content', methods=['POST'])
async def api_download():
    archive_path = create_zip_archive()

    return await send_file(
        archive_path,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename="sprites.zip"
    )
