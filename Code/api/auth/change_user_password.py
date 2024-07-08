from api.auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_manager import CAN_CHANGE_PASSWORD


@auth_bp.route('/change_user_password', methods=['POST'])
async def change_user_password():
    try:
        data = await request.get_json()

        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400

        if 'new_password' not in data:
            return jsonify({'message': 'Field "new_password" is required'}), 400

        if 'requester_token' not in data:
            return jsonify({'message': 'Field "requester_token" is required'}), 400

        try:
            requester_login = await auth_manager.get_user_login(data['requester_token'])
            access = await auth_manager.get_user_access(data['requester_token'])

            if not access & CAN_CHANGE_PASSWORD and requester_login != data['login']:
                return jsonify({'message': 'Access denied'}), 403
        
        except ValueError as e:
            return jsonify({'message': str(e)}), 403

        await auth_manager.change_user_password(data['login'], data['new_password'])
        return jsonify({'message': 'Password changed successfully'}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 403

    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
