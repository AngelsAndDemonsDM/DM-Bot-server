from api.account.bp_reg import account_bp
from api.api_tools import check_required_fields, get_requester_token
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessFlags


@account_bp.route('/change_user_access', methods=['POST'])
async def api_change_user_access():
    try:
        requester_token = get_requester_token(request.headers)
        data = await request.get_json()

        missing_fields = check_required_fields(data, "login", "new_access")
        if missing_fields:
            return jsonify({'message': f'Field(s) {missing_fields} are required'}), 400

        target_login = data['login']
        new_target_access = data['new_access']

        if not isinstance(new_target_access, dict):
            return jsonify({'message': 'Field "new_access" must be a dictionary'}), 400

        user_access: AccessFlags = await auth_manager.get_user_access_by_token(requester_token)
        if not user_access["change_access"]:
            return jsonify({'message': 'Access denied'}), 403

        target_access: AccessFlags = await auth_manager.get_user_access_by_login(target_login)

        for flag, value in new_target_access.items():
            if not isinstance(flag, str) or not isinstance(value, bool):
                return jsonify({'message': 'Field "new_access" must be a dictionary with string keys and boolean values'}), 400
            
            if not user_access[flag]:
                return jsonify({'message': f'Cannot grant access level for flag: {flag}'}), 403
            
            target_access.set_flag(flag, value)

        await auth_manager.change_user_access(target_login, target_access)
        return jsonify({'message': 'Access level changed successfully'}), 200

    except ValueError:
        return jsonify({'message': 'Access denied'}), 403
    
    except Exception as err:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(err)}), 500
