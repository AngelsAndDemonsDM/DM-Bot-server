from api.auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_manager import CAN_CHANGE_ACCESS


@auth_bp.route('/change_user_access', methods=['POST'])
async def change_user_access():
    try:
        data = await request.get_json()

        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400

        if 'new_access' not in data:
            return jsonify({'message': 'Field "new_access" is required'}), 400

        if 'requester_token' not in data:
            return jsonify({'message': 'Field "requester_token" is required'}), 400

        try:
            access = await auth_manager.get_user_access(data['requester_token'])
            if not access & CAN_CHANGE_ACCESS:
                return jsonify({'message': 'Access denied'}), 403
        
        except ValueError as e:
            return jsonify({'message': str(e)}), 403

        await auth_manager.change_user_access(data['login'], data['new_access'])
        return jsonify({'message': 'Access level changed successfully'}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 403

    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
