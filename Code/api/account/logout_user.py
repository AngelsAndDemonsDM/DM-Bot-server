from api.account.bp_reg import account_bp
from api.api_tools import get_requester_info
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system.auth_manager import AuthError


@account_bp.route('/logout', methods=['POST'])
async def api_logout_user():
    try:
        try:
            requester_token, _, _ = await get_requester_info(request.headers)
        
        except AuthError:
            return jsonify({"message": "Access denied"}), 403
        
        except Exception as err:
            return jsonify({"message": "An unexpected error occurred", "error": str(err)}), 500
        
        await auth_manager.logout_user(requester_token)
        return jsonify({'message': 'Logout attempt was made'}), 202
        
    except ValueError:
        return jsonify({'message': 'Access denied'}), 403
    
    except Exception as err:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(err)}), 500
