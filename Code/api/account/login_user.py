from api.account.bp_reg import account_bp
from api.api_tools import get_required_fields, handle_request_errors
from main_impt import auth_manager
from quart import jsonify, request


@handle_request_errors
@account_bp.route('/login', methods=['POST'])
async def api_login_user():
    login, password = get_required_fields(await request.get_json(), "login", "password")

    token = await auth_manager.login_user(login, password)
    return jsonify({'message': 'Login successful', 'token': token}), 200
