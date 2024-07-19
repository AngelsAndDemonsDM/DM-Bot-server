from api.account.bp_reg import account_bp
from api.api_tools import catch_403_500, get_requester_info
from main_impt import auth_manager
from quart import jsonify, request


@catch_403_500
@account_bp.route('/delete_user', methods=['POST'])
async def api_delete_user():
    _, _, requester_accses = await get_requester_info(request.headers)
        
    if not requester_accses["delete_users"]:
        return jsonify({'message': 'Access denied'}), 403
        
    data = await request.get_json()

    if 'login' not in data:
        return jsonify({'message': 'Field "login" is required'}), 400

    target_login = data['login']

    await auth_manager.delete_user(target_login)
    return jsonify({'message': 'User deleted successfully'}), 200
