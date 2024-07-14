from api.server.bp_reg import server_bp
from quart import jsonify


@server_bp.route('/status', methods=['GET'])
async def get_status():
    return jsonify({"message": "Online"}), 200
