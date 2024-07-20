from api.account.bp_reg import account_bp
from api.api_tools import (get_requester_info, get_required_fields,
                           handle_request_errors)
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessError


@handle_request_errors
@account_bp.route('/change_user_password', methods=['POST'])
async def api_change_user_password():
    _, requester_login, requester_accses = await get_requester_info(request.headers)

    target_login, new_target_password = get_required_fields(await request.get_json(), "login", "new_password")

    if not requester_accses["change_password"] and requester_login != target_login:
        raise AccessError()

    await auth_manager.change_user_password(target_login, new_target_password)
    return jsonify({'message': 'Password changed successfully'}), 200
