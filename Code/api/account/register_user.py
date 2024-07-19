from api.account.bp_reg import account_bp
from api.api_tools import (catch_MissingFilds_Auth_Exception,
                           get_required_fields)
from main_impt import auth_manager
from quart import jsonify, request


@catch_MissingFilds_Auth_Exception
@account_bp.route('/register', methods=['POST'])
async def api_register_user():
    login, password = get_required_fields(await request.get_json(), "login", "password")

    token = await auth_manager.register_user(login, password)
    if token:
        return jsonify({'message': 'Register successful', 'token': token}), 200

    return jsonify({'message': 'Register failed'}), 500
