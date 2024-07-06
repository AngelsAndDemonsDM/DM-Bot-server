from auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request


@auth_bp.route('/login', methods=['POST'])
async def login():
    try:
        data = await request.get_json()
        
        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400
        
        if 'password' not in data:
            return jsonify({'message': 'Field "password" is required'}), 400
        
        token = await auth_manager.login_user(data['login'], data['password'])
        return jsonify({'message': 'Login successful', 'token': token}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 403
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
