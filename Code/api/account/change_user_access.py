from api.account.bp_reg import account_bp
from api.api_tools import (get_requester_info, get_required_fields,
                           handle_request_errors)
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessError, AccessFlags


@handle_request_errors
@account_bp.route('/change_user_access', methods=['POST'])
async def api_change_user_access():
    _, _, requester_accses = await get_requester_info(request.headers)
    
    if not requester_accses["change_access"]:
        raise AccessError()
    
    target_login, new_target_access = get_required_fields(await request.get_json(), "login", "new_access")

    if not isinstance(new_target_access, dict):
        return jsonify({'message': 'Field "new_access" must be a dictionary'}), 400

    target_access: AccessFlags = await auth_manager.get_user_access_by_login(target_login)

    for flag, value in new_target_access.items():
        if not isinstance(flag, str) or not isinstance(value, bool):
            return jsonify({'message': 'Field "new_access" must be a dictionary with string keys and boolean values'}), 400
        
        if not requester_accses[flag]:
            return jsonify({'message': f'Cannot grant access level for flag: {flag}'}), 403
        
        target_access.set_flag(flag, value)

    await auth_manager.change_user_access(target_login, target_access)
    return jsonify({'message': 'Access level changed successfully'}), 200
