from api.account.bp_reg import account_bp
from api.api_tools import (catch_403_500, check_required_fields,
                           get_requester_info)
from main_impt import auth_manager
from quart import jsonify, request


@catch_403_500
@account_bp.route('/change_user_password', methods=['POST'])
async def api_change_user_password():
    _, requester_login, requester_accses = await get_requester_info(request.headers)

    data = await request.get_json()

    missing_fields = check_required_fields(data, "login", "new_password")
    if missing_fields:
        return jsonify({'message': f'Field(s) {missing_fields} are required'}), 400

    target_login = data['login']
    new_target_password = data['new_password']

    if not requester_accses["change_password"] and requester_login != target_login:
        return jsonify({'message': 'Access denied'}), 403

    await auth_manager.change_user_password(target_login, new_target_password)
    return jsonify({'message': 'Password changed successfully'}), 200
