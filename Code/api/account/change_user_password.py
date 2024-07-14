from api.account.bp_reg import account_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessFlags


@account_bp.route('/change_user_password', methods=['POST'])
async def api_change_user_password():
    try:
        requester_token = request.headers.get('token')
        data = await request.get_json()

        required_fields = ['login', 'new_password']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'message': f'Field(s) {", ".join(missing_fields)} are required'}), 400

        target_login = data['login']
        new_target_password = data['new_password']

        requester_login = await auth_manager.get_user_login_by_token(requester_token)
        requester_access: AccessFlags = await auth_manager.get_user_access_by_token(requester_token)
        
        if not requester_access["change_password"] and requester_login != target_login:
            return jsonify({'message': 'Access denied'}), 403

        await auth_manager.change_user_password(target_login, new_target_password)
        return jsonify({'message': 'Password changed successfully'}), 200

    except ValueError:
        return jsonify({'message': 'Access denied'}), 403
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
