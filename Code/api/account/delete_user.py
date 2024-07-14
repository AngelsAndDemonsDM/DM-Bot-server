from api.account.bp_reg import account_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessFlags


@account_bp.route('/delete_user', methods=['POST'])
async def api_delete_user():
    try:
        requester_token = request.headers.get('token')
        data = await request.get_json()

        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400

        target_login = data['login']

        requester_access: AccessFlags = await auth_manager.get_user_access_by_token(requester_token)
        if not requester_access["delete_users"]:
            return jsonify({'message': 'Access denied'}), 403

        await auth_manager.delete_user(target_login)
        return jsonify({'message': 'User deleted successfully'}), 200

    except ValueError:
        return jsonify({'message': 'Access denied'}), 403
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
