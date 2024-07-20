from api.account.bp_reg import account_bp
from api.api_tools import get_requester_info, handle_request_errors
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_system import AccessError


@handle_request_errors
@account_bp.route('/delete_user', methods=['POST'])
async def api_delete_user():
    _, _, requester_accses = await get_requester_info(request.headers)
        
    if not requester_accses["delete_users"]:
        raise AccessError()
        
    data = await request.get_json()

    if 'login' not in data:
        return jsonify({'message': 'Field "login" is required'}), 400

    target_login = data['login']

    await auth_manager.delete_user(target_login)
    return jsonify({'message': 'User deleted successfully'}), 200
