from api.account.bp_reg import account_bp
from api.api_tools import (catch_MissingFilds_Auth_Exception,
                           get_required_fields)
from main_impt import auth_manager
from quart import jsonify, request


@catch_MissingFilds_Auth_Exception
@account_bp.route('/login', methods=['POST'])
async def api_login_user():
    data = await request.get_json()

    missing_fields = get_required_fields(data, "login", "password")
    if missing_fields:
        return jsonify({'message': f'Field(s) {missing_fields} are required'}), 400

    login = data['login']
    password = data['password']

    token = await auth_manager.login_user(login, password)
    return jsonify({'message': 'Login successful', 'token': token}), 200
