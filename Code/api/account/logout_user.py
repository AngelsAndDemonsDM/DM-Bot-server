from api.account.bp_reg import account_bp
from api.api_tools import catch_403_500, get_requester_info
from main_impt import auth_manager
from quart import jsonify, request


@catch_403_500
@account_bp.route('/logout', methods=['POST'])
async def api_logout_user():
    requester_token, _, _ = await get_requester_info(request.headers)
    
    await auth_manager.logout_user(requester_token)
    return jsonify({'message': 'Logout attempt was made'}), 202
