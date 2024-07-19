import os
import zipfile

from api.api_tools import get_requester_info
from api.server.bp_reg import server_bp
from quart import jsonify, request, send_file
from root_path import ROOT_PATH
from systems.access_system.auth_manager import AuthError


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

@server_bp.route('/download', methods=['POST'])
async def api_download():
    try:
        await get_requester_info(request.headers)
    
    except AuthError:
        return jsonify({"message": "Access denied"}), 403
    
    except Exception as err:
        return jsonify({"message": "An unexpected error occurred", "error": str(err)}), 500

    archive_path = create_zip_archive()

    return await send_file(
        archive_path,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename="sprites.zip"
    )
