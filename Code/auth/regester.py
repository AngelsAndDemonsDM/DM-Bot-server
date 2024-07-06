from auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request


@auth_bp.route('/register', methods=['POST'])
async def register():
    try:
        data = await request.get_json()
        
        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400
        
        if 'password' not in data:
            return jsonify({'message': 'Field "password" is required'}), 400
        
        token = await auth_manager.register_user(data['login'], data['password'])
        
        if token:
            return jsonify({'message': 'Register successful', 'token': token}), 200
        else:
            return jsonify({'message': 'Register failed'}), 500

    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
