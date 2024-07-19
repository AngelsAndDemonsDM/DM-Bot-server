from api.account.bp_reg import account_bp
from api.api_tools import get_requester_info
from main_impt import auth_manager
from quart import jsonify, request

from Code.systems.access_system.auth_manager import AuthError


@account_bp.route('/access_flags', methods=['POST'])
async def api_access_flags():
    try:
        _, _, requester_accses = await get_requester_info(request.headers)
    
    except AuthError:
        return jsonify({"message": "Access denied"}), 403
    
    except Exception as err:
        return jsonify({"message": "An unexpected error occurred", "error": str(err)}), 500

    return jsonify(requester_accses._flags), 200 # Ай, ай, так низя, но мне похеру =)
