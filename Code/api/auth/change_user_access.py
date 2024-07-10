from auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_manager import AccessFlags


@auth_bp.route('/change_user_access', methods=['POST'])
async def change_user_access():
    try:
        ПОФИКСИТЬ БЛЯТЬ
        data = await request.get_json()

        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400

        if 'new_access' not in data:
            return jsonify({'message': 'Field "new_access" is required'}), 400

        if 'requester_token' not in data:
            return jsonify({'message': 'Field "requester_token" is required'}), 400

        try:
            requester_access: AccessFlags = await auth_manager.get_user_access(data['requester_token'])
            if not requester_access["change_access"]:
                return jsonify({'message': 'Access denied'}), 403

            new_access_flags = data['new_access']
            if not isinstance(new_access_flags, dict):
                return jsonify({'message': 'Field "new_access" must be a dictionary'}), 400

            for flag, value in new_access_flags.items():
                if flag not in requester_access._flags or requester_access[flag] is False:
                    return jsonify({'message': f'Cannot grant access level for flag: {flag}'}), 403

        except ValueError as e:
            return jsonify({'message': str(e)}), 403

        await auth_manager.change_user_access(data['login'], new_access_flags)
        return jsonify({'message': 'Access level changed successfully'}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 403

    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
