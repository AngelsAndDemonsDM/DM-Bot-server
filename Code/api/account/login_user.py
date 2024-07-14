from api.account.bp_reg import account_bp
from main_impt import auth_manager
from quart import jsonify, request


@account_bp.route('/login', methods=['POST'])
async def api_login_user():
    try:
        data = await request.get_json()

        required_fields = ['login', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'message': f'Field(s) {", ".join(missing_fields)} are required'}), 400

        login = data['login']
        password = data['password']

        try:
            token = await auth_manager.login_user(login, password)
            return jsonify({'message': 'Login successful', 'token': token}), 200
        
        except ValueError:
            return jsonify({'message': 'Access denied'}), 403

    except Exception as err:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(err)}), 500
