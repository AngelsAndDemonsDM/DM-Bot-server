from api.account.bp_reg import account_bp
from api.api_tools import check_required_fields
from main_impt import auth_manager
from quart import jsonify, request


@account_bp.route('/register', methods=['POST'])
async def api_register_user():
    try:
        data = await request.get_json()

        missing_fields = check_required_fields(data, "login", "password")
        if missing_fields:
            return jsonify({'message': f'Field(s) {missing_fields} are required'}), 400

        login = data['login']
        password = data['password']

        token = await auth_manager.register_user(login, password)
        if token:
            return jsonify({'message': 'Register successful', 'token': token}), 200

        return jsonify({'message': 'Register failed'}), 500
        

    except Exception as err:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(err)}), 500
