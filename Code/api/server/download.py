import os
import zipfile

from api.api_tools import catch_MissingFilds_Auth_Exception, get_requester_info
from api.server.bp_reg import server_bp
from quart import request, send_file
from root_path import ROOT_PATH


def create_zip_archive(): # TODO Проверка хеша архива
    folder_path = os.path.join(ROOT_PATH, "Sprites")
    archive_path = os.path.join(ROOT_PATH, "data", "sprites.zip")

    if not os.path.exists(archive_path):
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

    return archive_path

@catch_MissingFilds_Auth_Exception
@server_bp.route('/download', methods=['POST'])
async def api_download():
    await get_requester_info(request.headers)
    
    archive_path = create_zip_archive()

    return await send_file(
        archive_path,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename="sprites.zip"
    )
