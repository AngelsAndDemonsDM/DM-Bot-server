from auth.bp_reg import auth_bp
from flask import jsonify, request
from main_impt import auth_manager


@auth_bp.route('/logout', methods=['POST'])
async def logout():
    data = await request.get_json()
    if not 'token' in data:
        return jsonify({'message': 'field "token" is required'}), 400
    
    await auth_manager.logout(data['token'])
    
    return jsonify({'message': 'Попытка логаута была выполена'}), 202
