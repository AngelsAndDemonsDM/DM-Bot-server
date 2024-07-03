from auth.bp_reg import auth_bp
from flask import jsonify, request
from main_impt import auth_manager

@auth_bp.route('/logout', methods=['POST'])
async def logout():
    data = await request.get_json()
    if not 'login' in data:
        return jsonify({'message': 'field "login" is required'}), 400
    
    if not 'password' in data:
        return jsonify({'message': 'field "password" is required'}), 400
    try:
        token = await auth_manager.register_user(data['login'], data['password'])
        if token:
            return jsonify({'message': 'regester sucsess', 'token': token}), 200
    except Exception:
        pass
    
    return jsonify({'message': 'regester falue'}), 500 
