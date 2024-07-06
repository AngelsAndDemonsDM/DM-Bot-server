from auth.bp_reg import auth_bp
from flask import jsonify, request
from main_impt import auth_manager


@auth_bp.route('/login', methods=['POST'])
async def login():
    data = await request.get_json()
    if not 'login' in data:
        return jsonify({'message': 'field "login" is required'}), 400

    if not 'password' in data:
        return jsonify({'message': 'field "password" is required'}), 400

    token = await auth_manager.login(data['login'], data['password'])
    
    if token:
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Логин или пароль не верны'}), 403
