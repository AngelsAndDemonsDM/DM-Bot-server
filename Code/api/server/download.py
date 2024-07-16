import os
import zipfile

from api.api_tools import get_requester_token
from api.server.bp_reg import server_bp
from main_impt import auth_manager
from quart import jsonify, request, send_file
from root_path import ROOT_PATH


def create_zip_archive():
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
    requester_token = get_requester_token(request.headers)

    try:
        await auth_manager.get_user_login_by_token(requester_token)
    
    except ValueError:
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
