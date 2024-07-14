from api.account.bp_reg import account_bp
from main_impt import auth_manager
from quart import jsonify, request


@account_bp.route('/logout', methods=['POST'])
async def api_logout_user():
    requester_token = request.headers.get('token')
    
    try:
        await auth_manager.logout_user(requester_token)
        return jsonify({'message': 'Logout attempt was made'}), 202
    
    except ValueError:
        return jsonify({'message': 'Access denied'}), 403
    
    except Exception as err:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(err)}), 500
