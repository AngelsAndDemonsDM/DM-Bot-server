from api.api_tools import get_requester_token
from api.server.bp_reg import server_bp
from main_impt import auth_manager
from quart import jsonify, request


@server_bp.route('/access_flags', methods=['POST'])
async def api_access_flags():
    requester_token = get_requester_token(request.headers)

    try:
        accses = await auth_manager.get_user_access_by_token(requester_token)
    
    except ValueError:
        return jsonify({"message": "Access denied"}), 403
    
    except Exception as err:
        return jsonify({"message": "An unexpected error occurred", "error": str(err)}), 500

    return jsonify(accses._flags), 200 # Ай, ай, так низя, но мне похеру =)
